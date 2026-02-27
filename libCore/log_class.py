import libCore.utils_class as luC
import datetime
import json

class log:

    def check_or_create_file_day(self, link_to_dir, date):
        if self.luC_.check_file_exist(link_to_dir) == False:
            self.luC_.error_with_reason("", True)
        link_complet = self.luC_.absolute_link(link_to_dir+date)
        if self.luC_.check_file_exist(link_complet) == False:
            self.luC_.file_open(link_complet, "w")
        return self.luC_.file_open(link_complet, "a+")
    
    def prepare_message(self, content, severity, function_call):
        for one_check in [content, severity, function_call]:
            if self.luC_.is_string(one_check) == False:
                self.luC_.error_with_reason("Variable is not string : prepare_message()", True)
        return json.dumps({"content" :  content, "severity" : severity, "function_call" : function_call, "timestamp" : str(datetime.datetime.now()) }, indent=3)

    def send_message(self, handle, json_message):
        handle.write(json_message+"\n")
        handle.close()

    def pipe_log(self, content = "Unknow", severity = "Unknow", function_call = "Unknow",link_to_dir = "log\\"):
        handle = self.check_or_create_file_day(link_to_dir, f"{self.date.year}_{self.date.month}_{self.date.day}.log.txt")
        json_message = self.prepare_message(content, severity, function_call)
        self.send_message(handle,json_message)
    
    def save_state(self, text, type_data = "Unknow", link = "saveState\\", ):
        handle = self.luC_.file_open(self.luC_.absolute_link(link)+f"{self.date.year}_{self.date.month}_{self.date.day}.savestate.txt","a+")
        total_article =  0
        for one_index in text:
            total_article += len(text[one_index])
        try :
            formated_send =  json.dumps({"time_job_id" : f"{self.date.minute}{self.date.second}{self.date.microsecond}", "type_data" : type_data, "total_article" : total_article,"data" : text})    
            handle.write(formated_send+"\n")
            self.pipe_log("A savestate is integrated with data.","INFO","log() : save_state()")
        except:
            self.pipe_log("A savestate could not be saved.","ERROR","log() : save_state()")
            self.luC_.error_with_reason("A savestate could not be saved :  save_state()")
        handle.close()

    def save_data_set(self, text, data, type_data = "Unknow", link = "dataset\\", ):
        handle = self.luC_.file_open(self.luC_.absolute_link(link)+f"{self.date.year}_{self.date.month}_{self.date.day}.dataset.txt","a+")
        try :
            if type(data) != int:
                data = len(data)
            formated_send =  json.dumps({"time_job_id" : f"{self.date.minute}{self.date.second}{self.date.microsecond}", "type_data" : type_data, "total_index" : data,"data" : text})    
            handle.write(formated_send+"\n")
            self.pipe_log("A savestate is integrated with data.","INFO","log() : save_data_set()")
        except:
            self.pipe_log("A savestate could not be saved.","ERROR","log() : save_data_set()")
            self.luC_.error_with_reason("A savestate could not be saved :  save_data_set()")
        handle.close()
       
    def __init__(self):
        self.luC_ = luC.utils()
        self.date = datetime.datetime.now()