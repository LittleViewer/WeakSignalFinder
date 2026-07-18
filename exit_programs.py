import atexit
import time

def exit_situation():
    print("WeakSignalFinder is Finnish..")
    time.sleep(1)
    print("Copyright (c) 2025-present LittleViewer & WeakSignalFinder Contributors\nGoodbye!")

def call_exit_all_time():
    atexit.register(exit_situation)
