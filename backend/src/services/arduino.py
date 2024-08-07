import websockets

async def connect_to_websocket(message):
    uri = "ws://192.168.0.13:5002/ws"

    try:
        async with websockets.connect(uri) as websocket:
            await websocket.send(message)
            print("sent data to WebSocket")
            return True
    except websockets.exceptions as e:
        print("Couldn't connect to websocket")
        return False