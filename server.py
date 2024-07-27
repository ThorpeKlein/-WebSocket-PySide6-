import asyncio
import websockets
import os


async def handle_connection(websocket, path):
    buffer = bytearray()
    file_name = "received_data"

    try:
        async for message in websocket:
            if isinstance(message, bytes):
                if message == b"END":
                    break
                buffer.extend(message)
                print(f"Received chunk of size: {len(message)} bytes")
            else:
                print(f"Received text message: {message}")
    except Exception as e:
        print(f"Error: {e}")

    if buffer:
        with open(file_name, "wb") as f:
            f.write(buffer)
        print(f"Received and saved file as {file_name}")

        with open(file_name, "rb") as f:
            while chunk := f.read(1024 * 1024):
                await websocket.send(chunk)
                print(f"Sent chunk of size: {len(chunk)} bytes")

        await websocket.send(b"END")
        print("Sent end marker")

        os.remove(file_name)
        print(f"Deleted the cached file {file_name}")

    else:
        print("No data received.")

    await websocket.send("File received and saved, and sent back")


start_server = websockets.serve(handle_connection, "localhost", 8765, max_size=None)

asyncio.get_event_loop().run_until_complete(start_server)
print("WebSocket server started on ws://localhost:8765")
asyncio.get_event_loop().run_forever()
