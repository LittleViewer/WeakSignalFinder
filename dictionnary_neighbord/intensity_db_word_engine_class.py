import libCore.utils_class as luC
import libCore.config_tool_class as ctC
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
        for one_jobid in jobid_read:
            prepare_request_read_jobid += f"('{one_jobid}','{datetime.datetime.now()}'),"
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
                
    def pipe_main_engine(self, all_data):
        all_list_prepare_request = self.prepare_request(all_data)
        self.sub_pipe_choice_request(all_list_prepare_request)

    def __init__(self, obj_db):
        self.obj_db_ = obj_db
        self.luC_ = luC.utils()
        self.ctC_ = ctC.config_toml_tool()