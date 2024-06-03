import asyncio
import websockets
import threading
import signal

clients = set()
server_thread = None
loop = None

async def echo(websocket, path):
    clients.add(websocket)
    try:
        async for message in websocket:
            print(f"Received message from client: {message}")
    finally:
        clients.remove(websocket)

async def send_message():
    global loop
    while True:
        message = input("Enter a message to send: ")
        if message.lower() == "exit":
            break
        tasks = []
        if clients:
            for client in clients:
                task = asyncio.create_task(client.send(message))
                tasks.append(task)
            await asyncio.wait(tasks)
        else:
            print("No clients connected")

    print("Stopping server...")
    loop.call_soon_threadsafe(loop.stop)  # Stop asyncio event loop
    server_thread.join()  # Wait for server thread to complete
    print("Server stopped.")

def start_server():
    global loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    start_server = websockets.serve(echo, "0.0.0.0", 8765)
    loop.run_until_complete(start_server)
    loop.run_forever()

def stop_server(signal, frame):
    global loop
    tasks = asyncio.all_tasks(loop=loop)
    for task in tasks:
        task.cancel()
    loop.call_soon_threadsafe(loop.stop)  # Stop asyncio event loop

if __name__ == "__main__":
    signal.signal(signal.SIGINT, stop_server)
    server_thread = threading.Thread(target=start_server)
    server_thread.start()
    asyncio.run(send_message())