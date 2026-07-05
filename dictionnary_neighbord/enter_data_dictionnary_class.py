from datetime import datetime
import routerClassPackage
import sqlite3
import datetime
import io

class enter_data_dictionnary:
    def connect_dabase(self):
        try :
            link_to_database = self.obj_class_router["config_toml_tool"]().key_return("path","database_dictionnary_sqlite","database")
            if self.obj_class_router["utils"]().is_type(str,link_to_database) == True:
                self.handle_dabase_ = sqlite3.connect(self.obj_class_router["utils"]().absolute_link(link_to_database))
                self.cursor_database_ = self.handle_dabase_.cursor()
            else :
                
                self.obj_class_router["log"]().pipe_log(f"The expected formats are not provided as input!","ERROR","enter_data_dictionnary() : connect_dabase()")
                self.obj_class_router["utils"]().error_with_reason("The expected formats are not provided as input in enter_data_dictionnary.connect_dabase()!",True)
        except:
            self.obj_class_router["log"]().pipe_log(f"An unexpected error occurs during the connection with the database!","ERROR","enter_data_dictionnary() : connect_dabase()")
            self.obj_class_router["utils"]().error_with_reason("An unexpected error occurs during the connection with the database in prepare_request.connect_dabase()!",True)
        return [self.handle_dabase_, self.cursor_database_]
    
    def already_read(self, all_filename_read):
        prepare_request = "INSERT INTO know_folder VALUES "
        for one_filename in all_filename_read:
            prepare_request = prepare_request + f"('{self.job_id}','{one_filename}'),"
        prepare_request = prepare_request[:-1]+";"
        if len(all_filename_read) != 0:
            self.cursor_database_.execute(prepare_request)
            self.handle_dabase_.commit()

    def is_file_read(self):
        all_file_name = []
        self.cursor_database_.execute("SELECT name_folder FROM know_folder;")
        data = self.cursor_database_.fetchall()
        
        for one_filename in data :
            array_filename = one_filename[0].split("/")
            array_filename = array_filename[len(array_filename)-1].split("\\")
            all_file_name.append(array_filename[len(array_filename)-1])
        
        return set(all_file_name)

    def insert_io_file_in_db(self, exist_array,buff_file):
        if len(exist_array) != 0:
            self.cursor_database_.execute(f"INSERT INTO last_seen VALUES {buff_file.getvalue()[:-1]};")
            buff_file.close()
            self.handle_dabase_.commit()
            print(f"[{datetime.datetime.now()}] - {len(exist_array)} save as already viewed in last seen.")
            self.obj_class_router["log"]().pipe_log(f"{len(exist_array)} save as already viewed in last seen.","INFO","enter_data_dictionnary() : insert_io_file_in_db()")

    def detect_new_world(self, list_all_word_db,list_all_word):
        word_is_not_db = []
        word_exist = []
        buff_word_exist = io.StringIO()
        for one_word_possible in list_all_word:
            if one_word_possible not in list_all_word_db:
                word_is_not_db.append(one_word_possible)
            else:
                word_exist.append(one_word_possible)
                buff_word_exist.write(f"('{datetime.datetime.now()}','{self.job_id}','central_word','{one_word_possible}'),")
        self.insert_io_file_in_db(word_exist,buff_word_exist)
        return [word_is_not_db, word_exist]
    
    def new_word_enter_db(self, word_is_not_db):
        prepare_request = "INSERT INTO word VALUES "
        counter = len(word_is_not_db)-1
        for one_tick in range(len(word_is_not_db)):
            prepare_request = prepare_request + f"('{word_is_not_db[one_tick]}','{self.job_id}')"
            if one_tick != counter:
                prepare_request = prepare_request + ", "
            else:
                prepare_request = prepare_request + ";"
        self.cursor_database_.execute(prepare_request)
        self.handle_dabase_.commit()
        print(f"[{datetime.datetime.now()}] - {counter+1} new words enter in database")
        self.obj_class_router["log"]().pipe_log(f"{counter+1} new words enter in the long-term dictionary!","INFO","enter_data_dictionnary() : new_word_enter_db()")

    def neighbor_enter_db(self, all_data):
        buff_exist = io.StringIO()
        link_exist = []
        number_enter = 0
        prepare_request = "INSERT INTO dictionnary (central_word, position_, word_neighbor, run_added) VALUES "
        for one_line in all_data :
            for one_part in all_data[one_line]:
                for one_word in all_data[one_line][one_part]:
                    self.cursor_database_.execute(f"SELECT * FROM dictionnary WHERE central_word = '{one_line}' AND word_neighbor = '{one_word}';")
                    check_is_exist = self.cursor_database_.fetchall()
                    if len(check_is_exist) == 0:
                        number_enter = number_enter + 1
                        prepare_request = prepare_request + f" ('{one_line}','{one_part}','{one_word}', '{self.job_id}'),"
                    else:
                        buff_exist.write(f"('{datetime.datetime.now()}','{self.job_id}','neighbord_word','{one_line}-{one_part}-{one_word}'),")
                        link_exist.append(f"{one_line}-{one_part}-{one_word}")
        self.insert_io_file_in_db(link_exist,buff_exist)
        prepare_request = prepare_request[:-1]+";"
        if number_enter != 0:
            self.cursor_database_.execute(prepare_request)
            self.handle_dabase_.commit()
            print(f"[{datetime.datetime.now()}] - {number_enter+1} new neighbords enter in database")
            self.obj_class_router["log"]().pipe_log(f"{number_enter+1} new neighbords enter in the long-term dictionary!","INFO","enter_data_dictionnary() : neighbor_enter_db()")

    def pipe_enter_data(self, all_data):
        self.cursor_database_.execute("SELECT word FROM word;")
        list_all_word_db = self.cursor_database_.fetchall()
        word_list_in_db = []
        for one_line in list_all_word_db :
            word_list_in_db.append(one_line[0])
        
        list_all_word = self.obj_class_router["utils"]().dict_to_two_list(all_data)
        all_word_classify = self.detect_new_world(set(word_list_in_db), list_all_word[0])
        
        if len(all_word_classify[0]) >= 1:
            self.new_word_enter_db(all_word_classify[0])
        if len(all_data) != 0:
            self.neighbor_enter_db(all_data)        


    def __init__(self, job_id):
        import libCore.config_tool_class as ctC;self.obj_class_router = routerClassPackage.routerFunctionPipe(ctC.config_toml_tool().key_return("parameter","start_file","global_program"))
        self.connect_dabase()
        self.job_id = job_id
