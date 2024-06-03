import asyncio
import websockets
import datetime

async def send_logs(websocket, path):
    while True:
        log_message = f"Log entry at {datetime.datetime.now()}"
        await websocket.send(log_message)
        await asyncio.sleep(5)  # Send a log message every 5 seconds

async def main():
    async with websockets.serve(send_logs, "0.0.0.0", 8765):
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())