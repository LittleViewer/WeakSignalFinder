import libCore.utils_class as luC
import libCore.config_tool_class as ctC
import libCore.log_class as llC
import sqlite3
import datetime

class enter_data_dictionnary:
    def connect_dabase(self):
        try :
            link_to_database = self.ctC_.key_return("path","database_dictionnary_sqlite","database")
            if self.luC_.is_type(str,link_to_database) == True:
                self.handle_dabase_ = sqlite3.connect(self.luC_.absolute_link(link_to_database))
                self.cursor_database_ = self.handle_dabase_.cursor()
            else :
                self.llC_.pipe_log(f"The expected formats are not provided as input!","ERROR","enter_data_dictionnary() : connect_dabase()")
                self.luC_.error_with_reason("The expected formats are not provided as input in enter_data_dictionnary.connect_dabase()!",True)
        except:
            self.llC_.pipe_log(f"An unexpected error occurs during the connection with the database!","ERROR","enter_data_dictionnary() : connect_dabase()")
            self.luC_.error_with_reason("An unexpected error occurs during the connection with the database in prepare_request.connect_dabase()!",True)

    def for_launch(self):
        self.cursor_database_.execute("SELECT * FROM run ORDER BY date_ DESC LIMIT 1;")
        date_db = self.cursor_database_.fetchall()[0][1].split("-")
        date_old = datetime.datetime(int(date_db[0]),int(date_db[1]),int(date_db[2]))
        date_now_complete = datetime.datetime.now()
        self.date_now = str(date_now_complete).split(" ")[0]
            
        diff_date = date_now_complete - date_old
        if diff_date.days >= self.ctC_.key_return("parameter","cooldown_day_launch_dictionnary","for_launch"):
            return True
        else :
            return False

    def enter_last_run(self):
        self.cursor_database_.execute(f"INSERT INTO run VALUES ('{self.job_id}','{self.date_now}');")
        self.handle_dabase_.commit()
    
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
    
    def detect_new_world(self, list_all_word_db,list_all_word):
        word_is_not_db = []
        word_exist = []
        for one_word_possible in list_all_word:
            if one_word_possible not in list_all_word_db:
                word_is_not_db.append(one_word_possible)
            else:
                word_exist.append(one_word_possible)
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
        self.llC_.pipe_log(f"{counter+1} new words enter in the long-term dictionary!","INFO","enter_data_dictionnary() : new_word_enter_db()")

    def neighbor_enter_db(self, all_data):
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
        prepare_request = prepare_request[:-1]+";"
        if number_enter != 0:
            self.cursor_database_.execute(prepare_request)
            self.handle_dabase_.commit()
            print(f"[{datetime.datetime.now()}] - {number_enter+1} new neighbords enter in database")
            self.llC_.pipe_log(f"{number_enter+1} new neighbords enter in the long-term dictionary!","INFO","enter_data_dictionnary() : neighbor_enter_db()")

    def pipe_enter_data(self, all_data):
        self.cursor_database_.execute("SELECT word FROM word;")
        list_all_word_db = self.cursor_database_.fetchall()
        word_list_in_db = []
        for one_line in list_all_word_db :
            word_list_in_db.append(one_line[0])
        list_all_word = self.luC_.dict_to_two_list(all_data)
        all_word_classify = self.detect_new_world(set(word_list_in_db), list_all_word[0])
        
        if len(all_word_classify[0]) >= 1:
            self.new_word_enter_db(all_word_classify[0])
        if len(all_data) != 0:
            self.neighbor_enter_db(all_data)        


    def __init__(self, job_id):
        self.luC_ = luC.utils()
        self.ctC_ = ctC.config_toml_tool()
        self.llC_ = llC.log()
        self.connect_dabase()
        self.job_id = job_id