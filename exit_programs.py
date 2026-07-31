import libCore.utils_class as utils
import atexit
import time


def exit_situation(list_path_dir_to_remove = ["libCore\\cache_service_wsf\\"]):
    print("WeakSignalFinder is Finnish..")
    for one_path in list_path_dir_to_remove:
        if utils.utils().check_file_exist(one_path) == True:
            utils.utils().delete_recusive_file(one_path)
    time.sleep(1)
    print("Copyright (c) 2025-present LittleViewer & WeakSignalFinder Contributors\nGoodbye!")

def call_exit_all_time():
    atexit.register(exit_situation)
