import asyncio
import arduino

def setCoffe(state):
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(arduino.connect_to_websocket(state))
        return True
    except Exception as e:
        print(e)
        return False

