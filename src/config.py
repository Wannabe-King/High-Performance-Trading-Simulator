"""
Configuration settings for the Trade Simulator
"""
import os
from dataclasses import dataclass
from typing import Dict, List, Optional

@dataclass
class ExchangeConfig:
    """Configuration for an exchange"""
    name: str
    websocket_url: str
    available_pairs: List[str]
    order_types: List[str]
    fee_tiers: Dict[str, Dict[str, float]]
    
# Exchange configurations
EXCHANGES = {
    "OKX": ExchangeConfig(
        name="OKX",
        websocket_url="wss://ws.gomarket-cpp.goquant.io/ws/l2-orderbook/okx/",
        available_pairs=["BTC-USDT-SWAP", "ETH-USDT-SWAP", "SOL-USDT-SWAP", "XRP-USDT-SWAP"],
        order_types=["Market", "Limit"],
        fee_tiers={
            "TEIR 0": {"maker": 0.0008, "taker": 0.0010},
            "TEIR 1": {"maker": 0.0007, "taker": 0.0009},
            "TEIR 2": {"maker": 0.0006, "taker": 0.0008},
            "TEIR 3": {"maker": 0.0005, "taker": 0.0007},
            "TEIR 4": {"maker": 0.0003, "taker": 0.0005},
            "TEIR 5": {"maker": 0.0000, "taker": 0.0003},
        }
    )
}

# Default values for simulation parameters
DEFAULT_EXCHANGE = "OKX"
DEFAULT_PAIR = "BTC-USDT-SWAP"
DEFAULT_ORDER_TYPE = "Market"
DEFAULT_QUANTITY = 100.0  # USD equivalent
DEFAULT_VOLATILITY = 0.02  # 2% daily volatility
DEFAULT_FEE_TIER = "TIER 0"

# UI Configuration
UI_REFRESH_RATE_MS = 100  # UI refresh rate in milliseconds
UI_WINDOW_TITLE = "High-Performance Trade Simulator USING OKX Data"
UI_WINDOW_SIZE = (1200, 800)

# Logging Configuration
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_FILE = "high_frequency_trade_simulator.log"

# Performance benchmarking
ENABLE_BENCHMARKING = True
BENCHMARK_INTERVAL_SEC = 10  # Benchmark reporting interval in seconds