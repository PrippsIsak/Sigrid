from concurrent.futures import CancelledError
import time
import threading
import datetime
import backend.src.services.coffee_machine

class TimeActionThread(threading.Thread):
    def __init__(self, time):
        super().__init__()
        self.time = time
        self._stop_event = threading.Event()
        
    def run(self):
        try:
            while not self._stop_event.is_set():
                current_time = time.localtime(time.time())
                if (datetime.time(hour=current_time.tm_hour, minute=current_time.tm_min)) == self.time:
                    util.coffee_machine.setCoffe('On')
                    self.stop()
        except CancelledError:
            print("Thread Cancelled")

    
    def stop(self):
        """Function stops thread"""
        self._stop_event.set()