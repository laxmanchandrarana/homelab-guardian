import asyncio
import json
import websockets


async def main():
    async with websockets.connect("ws://localhost:8008/ws") as ws:
        print("✅ Connected to Guardian WebSocket")

        while True:
            message = await ws.recv()

            try:
                print(json.dumps(json.loads(message), indent=2))
            except Exception:
                print(message)


asyncio.run(main())
