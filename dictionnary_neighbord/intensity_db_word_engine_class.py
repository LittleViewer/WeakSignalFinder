import libCore.utils_class as luC
import libCore.config_tool_class as ctC
import libCore.log_class as llC
import libCore.date_utils_tool_class as duC
import database_rss_run.prepare_request_class as prC
import datetime
import gc

class intensity_db_word_engine_class:
    def prepare_request(self, all_data):
        all_list_prepare_insert = []
        new_all_list_prepare_insert = []
        list_job_id = []
        for one_job_id in all_data:
            total_word = 0
            list_job_id.append(one_job_id)
            for one_word in all_data[one_job_id]:
                absolute_value = all_data[one_job_id][one_word]
                total_word += int(absolute_value)
                all_list_prepare_insert.append([one_job_id, one_word, absolute_value])
        
        index_list = 0
        for one_list in all_list_prepare_insert:
            all_list_prepare_insert[index_list].append(one_list[2]/total_word)
            index_list += 1
                
        self.list_job_id_ = set(list_job_id)
        return all_list_prepare_insert
    
    def insert_new_jobid_read(self, jobid_read):
        prepare_request_read_jobid = "INSERT INTO run_integrated_intensity_word(jobId,date) VALUES "
        date_ = str(datetime.datetime.now()).split(" ")
        for one_jobid in jobid_read:
            prepare_request_read_jobid += f"('{one_jobid}','{date_[0]}'),"
        self.obj_db_[1].execute(prepare_request_read_jobid[:-1]+";")
        self.obj_db_[0].commit()


    def sub_pipe_choice_request(self, all_list):
        know_word = []
        all_job_id = []
        self.obj_db_[1].execute(f"SELECT jobId FROM run_integrated_intensity_word;")
        temp_jobid = (self.obj_db_[1].fetchall())
        for one_jobid in temp_jobid:
            know_word.append(one_jobid[0])
        authorized_job_id = self.list_job_id_- set(know_word)
        know_word = set(know_word)
        start = "INSERT INTO intensity_word VALUES "
        prepare_request = start
        number_new_intensity = 0
        tick_batch = 0
        total_possible_value = len(all_list)
        for one_list in all_list:
            if one_list[0] in authorized_job_id:
                prepare_request += f"('{one_list[0]}','{one_list[1]}',{one_list[2]},{one_list[3]}),"
                number_new_intensity += 1
                tick_batch += 1
            if self.ctC_.key_return("parameter","batch_longer_list","optimize") == tick_batch or total_possible_value == number_new_intensity:
                if number_new_intensity != 0:
                    self.obj_db_[1].execute(prepare_request[:-1]+";")
                    self.obj_db_[0].commit()
                    del prepare_request
                    gc.collect()
                    prepare_request = start
                    tick_batch = 0
        if number_new_intensity != 0:
            self.insert_new_jobid_read(set(authorized_job_id))
            print(f"[{datetime.datetime.now()}] - {number_new_intensity} intensity saved in database")
            self.llC_.pipe_log(f"Intensity saved in database : {number_new_intensity}", "INFO", "intensity_db_word_engine_class")
    
    def select_with_multiple_where(self,cursor_db,table,column_name, column_where, array_where):
        prepare_request = f"SELECT {column_name} FROM {table} WHERE"
        for one_where in array_where:
            prepare_request += f" {column_where} LIKE '{one_where}%' OR"
        cursor_db.execute(prepare_request[:-3]+';')
        all_line = cursor_db.fetchall()
        return all_line            
    
    def calcul_multiple_intensity(self,table):
        dict_word = {}
        list_word = []
        self.obj_db_[1].execute(f"SELECT * FROM {table};")
        all_data = self.obj_db_[1].fetchall()
            
        if len(all_data) == 0 :
            self.llC_.pipe_log(f"No data found in database", "WARN", "intensity_db_word_engine_class() : select_with_multiple_where()")
            return False
        
        for one_line in all_data :
            if one_line[1] not in set(list_word):
                list_word.append(one_line[1])
                dict_word[one_line[1]] = {"total_occurence" : one_line[2], "total_relative_value" : one_line[3], "number_corpus" : 1, "total_relative_value_weighted" : 0}
            else :
                dict_word[one_line[1]]["total_occurence"] += one_line[2]
                dict_word[one_line[1]]["total_relative_value"] += one_line[3]
                dict_word[one_line[1]]["number_corpus"] += 1
        for one_line in list_word :
            dict_word[one_line]["total_relative_value_weighted"] = dict_word[one_line]["total_relative_value"] / dict_word[one_line]["number_corpus"]
        return dict_word
    
    def enter_in_db_multiple_intensity(self, dict_data,job_id):
        number_enter = 0
        prepare_request = "INSERT INTO multiple_intensity_word VALUES "
        for one_line in dict_data:
            number_enter += 1
            prepare_request += f"('{job_id}','{one_line}',{dict_data[one_line]['total_occurence']},{dict_data[one_line]['total_relative_value']},{dict_data[one_line]['number_corpus']},{dict_data[one_line]['total_relative_value_weighted']}),"
        self.obj_db_[1].execute(prepare_request[:-1]+';')
        self.obj_db_[0].commit()
        print(f"[{datetime.datetime.now()}] - {number_enter} multiple intensity saved in database")
        self.llC_.pipe_log(f"Multiple intensity saved in database : {number_enter}", "INFO", "intensity_db_word_engine_class() : enter_in_db_multiple_intensity()")

    def pipe_main_engine(self, all_data,job_id):
        try:
            all_list_prepare_request = self.prepare_request(all_data)
            self.sub_pipe_choice_request(all_list_prepare_request)
        except:
            self.llC_.pipe_log(f"Error to save intensity in database", "ERROR", "intensity_db_word_engine_class")
        for_launch = self.duC_.is_ready_date_to_run(self.obj_db_,"run_global_calcul_intensity","cooldown_day_launch_inter_calcul_intensit_word")
        if for_launch == True:
            list_data_available = self.duC_.time_delta_list(self.ctC_.key_return("parameter","cooldown_day_launch_inter_calcul_intensit_word","for_launch"))            
            if list_data_available == False:
                return False
            if self.ctC_.key_return("parameter","single_multiple_intensity_save","for_launch") == True:
                self.obj_db_[1].execute("SELECT COUNT(*) FROM multiple_intensity_word;")
                number_word_erase = self.obj_db_[1].fetchall()[0][0]
                self.obj_db_[1].execute("DELETE FROM multiple_intensity_word;")
                self.obj_db_[0].commit()
                self.llC_.pipe_log(f"Intensity table dropped in DB with {number_word_erase} words.", "INFO", "intensity_db_word_engine_class() : pipe_main_engine()")

            dict_data = self.calcul_multiple_intensity("intensity_word")
            
            if dict_data == False:
                return False
            self.enter_in_db_multiple_intensity(dict_data,job_id)
            self.duC_.enter_last_run(self.obj_db_,"run_global_calcul_intensity",job_id)

    def __init__(self, obj_db):
        self.obj_db_ = obj_db
        self.luC_ = luC.utils()
        self.ctC_ = ctC.config_toml_tool()
        self.llC_ = llC.log()
        self.duC_ = duC.date_utils_tool()
        self.prC_ = prC.prepare_request()