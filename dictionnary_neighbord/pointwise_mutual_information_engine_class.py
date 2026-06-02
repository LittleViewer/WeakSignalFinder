import datetime
import libCore.utils_class as luC
import datetime

class pointwise_mutual_information_engine_class:
    def prepare_request(self, all_data):
        all_list_prepare_insert = []
        new_all_list_prepare_insert = []
        for one_job_id in all_data:
            total_word = 0
            for one_word in all_data[one_job_id]:
                absolute_value = all_data[one_job_id][one_word]
                total_word += int(absolute_value)
                all_list_prepare_insert.append([one_job_id, one_word, absolute_value])
        
            for one_list in all_list_prepare_insert:
                one_list.append(one_list[2]/total_word)
                new_all_list_prepare_insert.append(one_list.copy())
        return new_all_list_prepare_insert
    
    def sub_pipe_choice_request(self, all_list):
        know_word = []
        prepare_request = "INSERT INTO intensity_word VALUES "
        number_new_intensity = 0
        for one_list in all_list:
            if one_list[1] not in set(know_word):
                self.obj_db_[1].execute(f"SELECT * FROM intensity_word WHERE word = '{one_list[1]}' and jobId = '{one_list[0]}'")
                is_already_enter = self.obj_db_[1].fetchall()
                if len(is_already_enter) == 0:
                    prepare_request += f"('{one_list[0]}','{one_list[1]}',{one_list[2]},{one_list[3]}),"
                    number_new_intensity += 1
        if number_new_intensity != 0:
            self.obj_db_[1].execute(prepare_request[:-1]+";")
            self.obj_db_[0].commit()
            print(f"[{datetime.datetime.now()} {number_new_intensity} intensity saved in database]")

                
    def pipe_main_engine(self, all_data):
        all_list_prepare_request = self.prepare_request(all_data)
        self.sub_pipe_choice_request(all_list_prepare_request)

    def __init__(self, obj_db):
        self.obj_db_ = obj_db
        self.luC_ = luC.utils()