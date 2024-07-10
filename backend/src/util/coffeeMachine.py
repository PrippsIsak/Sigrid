import asyncio
import backend.src.services.arduino as arduino
from main import THREAD_POOL_MANAGER

def set_coffee(state):
    """Turn on or off the coffe machine"""
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(arduino.connect_to_websocket(state))
        return True
    except Exception as e:
        print(e)
        return False
    
def set_coffee_timer(state, time):
    """Starts a thread to keep track of the alarm"""
    try:
        if state:
            THREAD_POOL_MANAGER.submit_task(time)
            return 'OK', None, 'ON'
    
        THREAD_POOL_MANAGER.close_task(time)
        return 'OK', None, 'OFF'

    except Exception as e:
        return 'NOT OK', e, None
