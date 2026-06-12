import libCore.utils_class as luC
import libCore.config_tool_class as ctC
import datetime
import time

class verbose_initialize:

    def template_sub_pipe(self, list_path, type_ = "Unknow"):
        number_initialize = 0
        prepare_message = f"{type_} initialize (0/{len(list_path)})"
        print(prepare_message)
        for one_list_path in list_path:
            is_exist = self.luC_.check_file_exist(one_list_path)
            if is_exist == True:
                old_number = str(number_initialize)
                number_initialize += 1
                prepare_message = prepare_message.replace(old_number, str(number_initialize))
                self.luC_.rewrite_in_console_line()
                print(prepare_message)
            else:
                print(f"[{datetime.datetime.now()} - One of the {type_} does not exist!]")

    def check_db(self):
        list_path_db = [self.luC_.absolute_link(self.ctC_.key_return("path","database_run_sqlite","database")),self.luC_.absolute_link(self.ctC_.key_return("path","database_dictionnary_sqlite","database"))]
        self.template_sub_pipe(list_path_db, "Database")

    def check_file(self):
        list_path_file = [self.luC_.absolute_link(self.ctC_.key_return("path","extract_feed_Path","class_feed")), self.luC_.absolute_link(self.ctC_.key_return("path","file_model","prepare_data")), self.luC_.absolute_link(self.ctC_.key_return("path","file_stopword","prepare_data")), self.luC_.absolute_link(self.ctC_.key_return("path","exclude_file","read_data_dictionnary"))]
        self.template_sub_pipe(list_path_file, "File")

    def welcome_message(self):
        print(f"Welcome to Weak Signal Finder !\n{datetime.datetime.today()} - {datetime.datetime.now().time().replace(microsecond=0)}\nCopyright (c) 2025-present LittleViewer & WeakSignalFinder Contributors")
        time.sleep(1)

    def pipe_verbose_initialize(self):
        self.check_db()
        self.check_file()
        self.welcome_message()

    def __init__(self):
        self.luC_ = luC.utils()
        self.ctC_ = ctC.config_toml_tool()