# src/ui/input_panel.py

import tkinter as tk
from tkinter import ttk

class LeftPanel:
    def __init__(self, parent):
        self.frame = ttk.LabelFrame(parent, text="Input Parameters")

        self.exchange = ttk.Combobox(self.frame, values=["OKX"], state="readonly")
        self.exchange.set("OKX")

        self.asset = ttk.Entry(self.frame)
        self.asset.insert(0, "BTC-USDT")

        self.quantity = ttk.Entry(self.frame)
        self.quantity.insert(0, "100")

        self.volatility = ttk.Entry(self.frame)
        self.volatility.insert(0, "0.05")

        self.fee_tier = ttk.Combobox(self.frame, values=["Tier 1", "Tier 2", "Tier 3"], state="readonly")
        self.fee_tier.set("Tier 1")

        # Layout
        ttk.Label(self.frame, text="Exchange:").pack(anchor="w")
        self.exchange.pack(fill="x")

        ttk.Label(self.frame, text="Asset:").pack(anchor="w")
        self.asset.pack(fill="x")

        ttk.Label(self.frame, text="Quantity (USD):").pack(anchor="w")
        self.quantity.pack(fill="x")

        ttk.Label(self.frame, text="Volatility:").pack(anchor="w")
        self.volatility.pack(fill="x")

        ttk.Label(self.frame, text="Fee Tier:").pack(anchor="w")
        self.fee_tier.pack(fill="x")
