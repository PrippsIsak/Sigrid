import asyncio
from services import arduino, thread_manager

def set_coffee(state):
    """Turn on or off the coffe machine"""
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(arduino.connect_to_websocket(state))
        return None
    except Exception as err:
        return err
    
def set_coffee_timer(state, time):
    """Starts a thread to keep track of the alarm"""
    try:
        if state:
            thread_manager.submit_task(time)
            return 'ON', None
    
        thread_manager.close_task(time)
        return 'OFF', None

    except Exception as err:
        return None, err
