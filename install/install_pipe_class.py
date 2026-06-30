import libCore.config_tool_class as ctC
import libCore.utils_class as luC
import sqlite3
import datetime


class install_class:

    def database_read_script(self, path_db, handle_file):
        connect_obj = sqlite3.connect(path_db)
        cursor_obj =  connect_obj.cursor()
        cursor_obj.executescript(handle_file.read())
        handle_file.close()
        cursor_obj.close()
        connect_obj.close()

    def pipe_install(self):
        dict_path = {"db":[self.ctC_.key_return("path","database_run_sqlite","database"),self.ctC_.key_return("path","database_dictionnary_sqlite","database")]}
        dict_schema_db = self.ctC_.key_return("parameter","initial_schema","install")
        for one_type_path in dict_path:
            for one_path in dict_path[one_type_path]:
                all_parts_link  = self.luC_.absolute_link(one_path).parts
                part = ""
                tick = 0
                max_part = len(all_parts_link) - 1 
                for one_part in all_parts_link:
                    if max_part == tick or tick == 0:
                        separator = ""
                    else:
                        separator = "\\"

                    part += one_part+separator
                    
                    if self.luC_.check_file_exist(self.luC_.absolute_link(part)) ==  False:
                        path = self.luC_.absolute_link(part)
                        if max_part == tick:
                            self.luC_.file_open(path,"a")
                            handle_schema = all_parts_link[len(all_parts_link)-1].split(".")
                            
                            if handle_schema[len(handle_schema)-1] == "db":
                                handle =  self.luC_.file_open(self.luC_.absolute_link(dict_schema_db[handle_schema[0]]))
                                self.database_read_script(path, handle)
                                
                        else:
                            self.luC_.create_dir(path)

                    tick +=1
        print(f"[{self.date_}] - Weak Signal Finder installation is complete: Please restart the program.")

    def __init__(self):
        self.ctC_ = ctC.config_toml_tool()
        self.luC_ = luC.utils()
        self.date_ = str(datetime.datetime.now()).split(".")[0]
