import libCore.utils_class as luC
import libCore.config_tool_class as ctC
import datetime
import socket
import time
import sys
import os

class verbose_initialize:

    def template_sub_pipe(self, list_path, type_ = "Unknow"):
        number_initialize = 0
        if self.accept_verbose_ == True:
            prepare_message = f"{type_} initialize (0/{len(list_path)})"
            print(prepare_message)
        for one_list_path in list_path:
            is_exist = self.luC_.check_file_exist(one_list_path)
            datetime_ = str(datetime.datetime.now()).split('.')[0]
            if is_exist == True:
                old_number = str(number_initialize)
                number_initialize += 1
                
                if self.accept_verbose_ == True:
                    prepare_message = prepare_message.replace(old_number, str(number_initialize))
                    self.luC_.rewrite_in_console_line()
                    print(prepare_message)
                size_object = os.path.getsize(one_list_path)
                if size_object/1073741824 >= 2.1:
                    print(f"[{datetime_}] - Warning you're object in {str(one_list_path)} is extremly heavy (more 2 gigabytes)!") 
            else:
                print(f"[{datetime_} - One of the {type_} does not exist!]")
                sys.exit()



    def check_db(self):
        list_path_db = [self.luC_.absolute_link(self.ctC_.key_return("path","database_run_sqlite","database")),self.luC_.absolute_link(self.ctC_.key_return("path","database_dictionnary_sqlite","database"))]
        self.template_sub_pipe(list_path_db, "Database")

    def check_file(self):
        list_path_file = [self.luC_.absolute_link(self.ctC_.key_return("path","extract_feed_Path","class_feed")), self.luC_.absolute_link(self.ctC_.key_return("path","file_model","prepare_data")), self.luC_.absolute_link(self.ctC_.key_return("path","file_stopword","prepare_data")), self.luC_.absolute_link(self.ctC_.key_return("path","exclude_file","read_data_dictionnary"))]
        self.template_sub_pipe(list_path_file, "File")

    def check_internet(self, timeout = 3):
        try :
            start_check = time.perf_counter()
            socket.setdefaulttimeout(timeout)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(("www.google.com", 80))
            stop_check = time.perf_counter()
            if self.accept_verbose_ == True:
                print(f"Internet connection OK! : {round((stop_check - start_check) * 1000,2)}ms")
                time.sleep(0.5)
        except Exception:
            print(f"[{str(datetime.datetime.now()).split('.')[0]}] - No internet connection!")
            sys.exit()

    def welcome_message(self):
        print(f"Welcome to Weak Signal Finder !\n{str(datetime.datetime.today()).split(' ')[0]} - {str(datetime.datetime.now().time()).split('.')[0]}\nCopyright (c) 2025-present LittleViewer & WeakSignalFinder Contributors")
        if self.accept_verbose_ == True:
            time.sleep(1)

    def pipe_verbose_initialize(self,accept_verbose = True):
        self.accept_verbose_ = accept_verbose
        self.check_db()
        self.check_file()
        self.check_internet()
        self.welcome_message()

    def __init__(self):
        self.luC_ = luC.utils()
        self.ctC_ = ctC.config_toml_tool()