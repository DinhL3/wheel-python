import asyncio
from bleak import BleakClient

# Replace this with the Bluetooth address of your micro:bit
MICROBIT_ADDRESS = "F5:40:E8:8B:43:29"

# UUID for the UART RX characteristic
UART_RX_CHARACTERISTIC_UUID = "6e400003-b5a3-f393-e0a9-e50e24dcca9e"

def handle_rx(_: int, data: bytearray):
    print("Received:", data.decode("utf-8").strip())

async def main(address):
    async with BleakClient(address) as client:
        print("Connected to micro:bit")
        await client.start_notify(UART_RX_CHARACTERISTIC_UUID, handle_rx)
        print("Notification started. Waiting for data...")

        # Keep the connection alive to continue receiving data
        while True:
            await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main(MICROBIT_ADDRESS))

#NOTIFICATION_CHARACTERISTIC_UUID = "e95d9775-251d-470a-a062-fa1922dfa9a8"