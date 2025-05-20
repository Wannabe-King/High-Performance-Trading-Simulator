# src/data/websocket_manager.py

import asyncio
import websockets
import json
import logging
from datetime import datetime

class WebSocketManager:
    def __init__(self, url, symbol="BTC-USDT", on_message=None):
        self.url = url
        self.symbol = symbol
        self.ws = None
        self.on_message = on_message  # Callback to process messages

    async def connect(self):
        try:
            async with websockets.connect(self.url) as websocket:
                self.ws = websocket
                logging.info("Connected to WebSocket")
                await self.subscribe()
                await self.receive()
        except Exception as e:
            logging.error(f"WebSocket connection error: {e}")

    async def subscribe(self):
        payload = {
            "op": "subscribe",
            "args": [
                {
                    "channel": "books",
                    "instId": self.symbol
                }
            ]
        }
        await self.ws.send(json.dumps(payload))
        logging.info(f"Subscribed to {self.symbol} orderbook")

    async def receive(self):
        async for message in self.ws:
            try:
                data = json.loads(message)
                if self.on_message:
                    await self.on_message(data)
            except Exception as e:
                logging.error(f"Failed to process message: {e}")

    def run(self):
        asyncio.run(self.connect())
