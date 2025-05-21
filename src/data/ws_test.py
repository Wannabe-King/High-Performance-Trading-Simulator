# test_ws.py (run this for testing)

from src.data.ws_backend import WebSocketManager
import asyncio

async def handle_message(data):
    if "asks" in data and "bids" in data:
        print("Top Ask:", data["asks"][0])
        print("Top Bid:", data["bids"][0])
        print("Timestamp:", data.get("timestamp"))

if __name__ == "__main__":
    ws_url = "wss://ws.gomarket-cpp.goquant.io/ws/l2-orderbook/okx/BTC-USDT-SWAP"
    manager = WebSocketManager(url=ws_url, on_message=handle_message)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(manager.run())
