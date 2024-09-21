"""
Reload the python script when files in the src directory change.
"""

import sys
import subprocess
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

PROCESS = None

def relaunch():
    global PROCESS
    if PROCESS is not None:
        PROCESS.kill()
    PROCESS = subprocess.Popen(['python3', sys.argv[1]])

class Handler(FileSystemEventHandler):
    @staticmethod
    def on_modified(event):
        relaunch()

    @staticmethod
    def on_created(event):
        relaunch()

def watch():
    observer = Observer()
    event_handler = Handler()
    observer.schedule(event_handler, 'src', recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == '__main__':
    relaunch()
    watch()