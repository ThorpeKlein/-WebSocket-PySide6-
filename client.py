import asyncio
import websockets


async def send_file_and_receive_response(file_path):
    uri = "ws://localhost:8765"
    async with websockets.connect(uri, max_size=None) as websocket:

        with open("example.mp4", "rb") as f:
            while chunk := f.read(1024 * 1024):
                await websocket.send(chunk)
                print(f"Sent chunk of size: {len(chunk)} bytes")


        await websocket.send(b"END")
        print("Sent end marker")


        buffer = bytearray()
        async for message in websocket:
            if isinstance(message, bytes):
                if message == b"END":
                    break
                buffer.extend(message)
                print(f"Received chunk of size: {len(message)} bytes")
            else:
                print(f"Received text message: {message}")
                break


        if buffer:
            received_file_path = "received_from_server.mp4"
            with open(received_file_path, "ab") as f:
                f.write(buffer)
            print(f"Received and saved file as {received_file_path}")
        else:
            print("No response data received.")


asyncio.get_event_loop().run_until_complete(send_file_and_receive_response("example.mp4"))
