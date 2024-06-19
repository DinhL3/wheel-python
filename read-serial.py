import serial
import asyncio
import websockets
import re

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
                    # Extract the number from the message
                    number = extract_number_from_message(line)
                    if number is not None:
                        await notify_clients(number)
            await asyncio.sleep(0.1)  # Add a small sleep to prevent high CPU usage
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        ser.close()

def extract_number_from_message(message):
    # Using regex to extract the number
    match = re.search(r'\d+', message)
    return match.group(0) if match else None

async def notify_clients(message):
    if clients:
        await asyncio.gather(*[client.send(message) for client in clients])

async def handle_client(websocket, path):
    global ser  # Declare ser as global to send reset command
    # Register client
    clients.add(websocket)
    try:
        async for message in websocket:
            if message == "reset":
                print("Received reset command from client")
                ser.write(b'reset\n')  # Send reset command to Arduino
            # For now, we are not handling any other incoming messages from clients
    finally:
        # Unregister client
        clients.remove(websocket)

async def main():
    global ser  # Declare ser as global to use it in handle_client
    # Initialize the serial connection
    # Change this to the port of your Arduino
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    ser.flush()

    # Start the serial reading task
    serial_task = asyncio.create_task(read_from_serial(ser))

    # Start the WebSocket server
    async with websockets.serve(handle_client, "0.0.0.0", 8765):
        await serial_task  # Run the serial task indefinitely

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Program interrupted by user.")