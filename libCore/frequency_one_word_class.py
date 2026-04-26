import libCore.utils_class as luC
import libCore.log_class as llC
import database.prepare_request_class as prC
import datetime
import json

class frequency_one_word:

    def add_word_intensity(self, word, word_intensity, value_add = 1):
        word_intensity[word] = word_intensity[word] + value_add
        return word_intensity

    def word_claimer(self, word, word_claim, word_intensity):
        if word in set(word_claim):
           word_claim = self.add_word_intensity(word, word_intensity)
        else: 
            word_claim.append(word)
            word_intensity[word] = 1
        return word_intensity

    def delete_little_intensity(self, word_intensity_dict, filter):
        word_intensity_dict_clean = word_intensity_dict.copy()
        for one_index in word_intensity_dict:
            if word_intensity_dict[one_index] <= filter:
                del(word_intensity_dict_clean[one_index])
        return word_intensity_dict_clean

    def pipe_frequency_one_word(self, data, obj_database,job_id, filter = 1):
        word_claim = []
        word_intensity = {}
        for one_index in data:
            for one_bloc in data[one_index]:
                for one_word in one_bloc:
                    word_intensity = self.word_claimer(one_word, word_claim, word_intensity)
        word_intensity_clean = self.delete_little_intensity(word_intensity, filter)
        self.llC_.save_data_set((word_intensity_clean), word_intensity_clean, "word_intensity")
        self.prC_.insert_data_database(obj_database[0],obj_database[1],"saveData",["jobId","dateTime","type","data"],[[job_id,datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),"saveStateWordIntensity",str(word_intensity_clean).replace("'",'"')]])
        self.llC_.pipe_log("The word intensity is calculated as well as saved in the dataset.","INFO","frequency_one_word() : pipe_frequency_one_word()")
        return word_intensity_clean

    def __init__(self):
        self.luC_ = luC.utils()
        self.llC_ =  llC.log()
        self.prC_ = prC.prepare_request()