import serial
import asyncio
import websockets

# Global variable to store WebSocket connections
clients = set()

async def read_from_serial(ser):
    system_ready = False  # Flag to check if system is ready
    try:
        while True:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').rstrip()
                if "System ready" in line:
                    print("Arduino:", line)
                    system_ready = True  # Set the flag when "System ready" is received
                    await notify_clients(line)
                elif system_ready:
                    # Only send other messages after the system is ready
                    print("Arduino:", line)
                    await notify_clients(line)
            await asyncio.sleep(0.1)  # Add a small sleep to prevent high CPU usage
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        ser.close()

async def notify_clients(message):
    if clients:
        await asyncio.wait([client.send(message) for client in clients])

async def websocket_handler(websocket, path):
    # Register the client
    clients.add(websocket)
    try:
        async for message in websocket:
            # Handle incoming messages from the client if needed
            pass
    finally:
        # Unregister the client
        clients.remove(websocket)

async def main():
    # Initialize the serial connection
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.flush()

    # Start the serial reading task
    serial_task = asyncio.create_task(read_from_serial(ser))

    # Start the WebSocket server
    async with websockets.serve(websocket_handler, "0.0.0.0", 8765):
        await serial_task  # Keep the program running by awaiting the serial task

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Program interrupted by user.")
