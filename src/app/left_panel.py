# src/ui/left_panel.py

import tkinter as tk
import asyncio
from src.data.ws_backend import WebSocketManager
from src.models.spillage import SlippageModel
import time
from datetime import datetime,timezone
from tkinter import ttk
from src.models.fee_model import FeeModel
from src.models.maker_taker_model import MakerTakerModel
from src.models.market_impact import MarketImpactModel
import threading
from src.config import (
    EXCHANGES,
    DEFAULT_EXCHANGE,
    DEFAULT_PAIR,
    DEFAULT_ORDER_TYPE,
    DEFAULT_QUANTITY,
    DEFAULT_VOLATILITY,
    DEFAULT_FEE_TIER,
)

class LeftPanel:
    def __init__(self, parent,orderbook_panel,output_panel):
        self.frame = ttk.LabelFrame(parent, text="Input Parameters", padding=10)
        self.orderbook_panel = orderbook_panel
        self.output_panel=output_panel
        self.slippage_model= SlippageModel()
        self.simulation_running = False  # New flag to track simulation state
        self.ws_manager = None
        self.last_received_time = time.time()
        self.fee_model = FeeModel()
        self.maker_taker_model = MakerTakerModel()
        self.impact_model = MarketImpactModel()


        # Exchange dropdown
        ttk.Label(self.frame, text="Exchange:").grid(row=0, column=0, sticky="w",pady=5)
        self.exchange_var = tk.StringVar(value=DEFAULT_EXCHANGE)
        self.exchange_menu = ttk.Combobox(self.frame, textvariable=self.exchange_var, values=list(EXCHANGES.keys()), state="readonly")
        self.exchange_menu.grid(row=0, column=1, sticky="ew")

        # Asset Pair dropdown
        ttk.Label(self.frame, text="Asset Pair:").grid(row=1, column=0, sticky="w",pady=5)
        self.pair_var = tk.StringVar(value=DEFAULT_PAIR)
        self.pair_menu = ttk.Combobox(self.frame, textvariable=self.pair_var, values=EXCHANGES[DEFAULT_EXCHANGE].available_pairs, state="readonly")
        self.pair_menu.grid(row=1, column=1, sticky="ew")

        # Order Type dropdown
        ttk.Label(self.frame, text="Order Type:").grid(row=2, column=0, sticky="nw",pady=5)
        self.order_type_var = tk.StringVar(value=DEFAULT_ORDER_TYPE.lower())  # Ensure lowercase match

        order_types = EXCHANGES[DEFAULT_EXCHANGE].order_types
        order_type_frame = ttk.Frame(self.frame)

        for i, otype in enumerate(order_types):
            value = otype.lower()
            state="active"
            if(value=="limit"):
                state="disabled"
            ttk.Radiobutton(
                order_type_frame,
                text=otype.capitalize(),
                variable=self.order_type_var,
                value=value,
                state=state
            ).grid(row=0, column=i, padx=5)

        order_type_frame.grid(row=2, column=1, sticky="w")

        # Quantity input
        ttk.Label(self.frame, text="Quantity (USD):").grid(row=3, column=0, sticky="w",pady=5)
        self.quantity_var = tk.DoubleVar(value=DEFAULT_QUANTITY)
        self.quantity_entry = ttk.Entry(self.frame, textvariable=self.quantity_var)
        self.quantity_entry.grid(row=3, column=1, sticky="ew")

        # Volatility input
        ttk.Label(self.frame, text="Volatility (%):").grid(row=4, column=0, sticky="w",pady=5)
        self.volatility_var = tk.DoubleVar(value=DEFAULT_VOLATILITY * 100)  # shown as percent
        self.volatility_entry = ttk.Entry(self.frame, textvariable=self.volatility_var)
        self.volatility_entry.grid(row=4, column=1, sticky="ew")

        # Fee Tier dropdown
        ttk.Label(self.frame, text="Fee Tier:").grid(row=5, column=0, sticky="w",pady=5)
        self.fee_tier_var = tk.StringVar(value=DEFAULT_FEE_TIER)
        self.fee_tier_menu = ttk.Combobox(
            self.frame,
            textvariable=self.fee_tier_var,
            values=list(EXCHANGES[DEFAULT_EXCHANGE].fee_tiers.keys()),
            state="readonly"
        )
        self.fee_tier_menu.grid(row=5, column=1, sticky="ew")

        # Submit button (optional callback hook)
        self.submit_button = ttk.Button(self.frame, text="Start Simulation", command=self.toggle_simulation)
        self.submit_button.grid(row=6, column=0, columnspan=2, pady=10)

        # Column config
        self.frame.columnconfigure(1, weight=1)

        self.orderbook_panel = orderbook_panel
        self.orderbook_panel.frame.pack(side=tk.BOTTOM, fill=tk.BOTH, padx=10, pady=5)

    def toggle_simulation(self):
        if self.simulation_running:
            self.stop_simulation()
        else:
            self.start_simulation()

    def stop_simulation(self):
        if self.ws_manager:
            self.ws_manager.close()
            self.ws_manager = None

        self.simulation_running = False
        self.submit_button.config(text="Start Simulation")

    def get_inputs(self):
        return {
            "exchange": self.exchange_var.get(),
            "pair": self.pair_var.get(),
            "order_type": self.order_type_var.get(),
            "quantity": self.quantity_var.get(),
            "volatility": self.volatility_var.get() / 100,  # convert back to decimal
            "fee_tier": self.fee_tier_var.get(),
        }
    
    def start_simulation(self):
        inputs = self.get_inputs()
        exchange = inputs["exchange"]
        pair = inputs["pair"]
        ws_url = f"{EXCHANGES[exchange].websocket_url}{pair}"

        def handle_ws_message(message):
            self.frame.after(0, lambda: self.handle_orderbook_update(message))


        def run_ws():
            self.ws_manager = WebSocketManager(ws_url, symbol=pair, on_message=handle_ws_message)
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self.ws_manager.run())

        threading.Thread(target=run_ws, daemon=True).start()

        self.simulation_running = True
        self.submit_button.config(text="Stop Simulation")



    def on_close(self):
        if(self.ws_manager):
            self.stop_simulation()

    def handle_orderbook_update(self, data):
        def update_ui():
            try:

                now = time.time()
                latency_ms = round((now - self.last_received_time) * 1000,2)
                self.last_received_time = now

                # Directly using "asks" and "bids" from data
                if "asks" in data and "bids" in data:
                    bids = [(float(p), float(q)) for p, q in data["bids"][:10]]
                    asks = [(float(p), float(q)) for p, q in data["asks"][:10]]
                    self.orderbook_panel.update_orderbook(bids, asks)

                # --- Prepare features for slippage model ---
                top_bid = bids[0][0]
                top_ask = asks[0][0]
                mid_price = (top_bid + top_ask) / 2
                spread_pct = (top_ask - top_bid) / mid_price * 100
                # Calculate depths
                bid_depth = sum(q for _, q in bids)
                ask_depth = sum(q for _, q in asks)

                # These are also used for imbalance and depth ratio
                total_bid_qty = bid_depth
                total_ask_qty = ask_depth
                imbalance = total_bid_qty / (total_bid_qty + total_ask_qty)
                depth_ratio = min(total_bid_qty, total_ask_qty) / max(total_bid_qty, total_ask_qty)
                volatility = self.volatility_var.get() / 100
                quantity = self.quantity_var.get()

                model_input = {
                    "quantity": quantity,
                    "mid_price": mid_price,
                    "spread_pct": spread_pct,
                    "imbalance": imbalance,
                    "depth_ratio": depth_ratio,
                    "volatility": volatility,
                    "bid_depth": bid_depth,
                    "ask_depth": ask_depth,
                    "order_type": self.order_type_var.get()
                }

                # --- Use slippage model ---
                slippage = round(self.slippage_model.calculate(model_input), 4)
                # --- Use maker/taker model ---
                order_type = self.order_type_var.get()  # Assuming you have a dropdown for "limit"/"market"
                model_input["order_type"] = order_type
                maker_proportion = self.maker_taker_model.predict(model_input)
                # --- Use fee model ---
                fees = round(self.fee_model.calculate(quantity, mid_price, maker_proportion), 4)
                # --- Use market impact model ---
                impact = round(
                    self.impact_model.calculate(
                        quantity=quantity,
                        price=mid_price,
                        volatility=model_input["volatility"],
                        orderbook_data=model_input
                    ),
                    4
                )
                # --- Final net cost ---
                net_cost = round(slippage + fees + impact, 4)

                output_data = {
                    "Expected Slippage(%)": slippage,
                    "Expected Fees(USD)": fees,
                    "Market Impact(%)": impact,
                    "Net Cost(USD)": net_cost,
                    "Maker/Taker Proportion(out of 100%)": f"{int(maker_proportion * 100)}/{int((1 - maker_proportion) * 100)}",
                    "Internal Latency(ms)": latency_ms
                }

                self.output_panel.update(output_data)
            except Exception as e:
                print(f"Error in update_ui: {e}")
            

        

        self.frame.after(0, update_ui)

