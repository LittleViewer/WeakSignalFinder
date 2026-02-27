import libCore.utils_class as luC
import libCore.log_class as llC
import datetime
import json

class api_local:
    
    def open_file(self, link):
        handle = self.luC_.file_open(self.luC_.absolute_link(link)+f"{self.date.year}_{self.date.month}_{self.date.day}.local_api.txt","a+")
        return handle

    def write_value(self, intensity_word, contextual_neighborhood, word_central_neighborhood, handle):
        content_api = json.dumps({"time" : f"[{self.date}]", "time_jobid" : f"[{self.date.year}{self.date.month}{self.date.second}{self.date.microsecond}{self.date.day}]", "intensity_word" : intensity_word, "contextual_neighborhood" : contextual_neighborhood, "word_central_neighborhood" : word_central_neighborhood})
        handle.write(content_api)
    
    def pipe_api_local(self, intensity_word, contextual_neighborhood, word_central_neighborhood, link = "local_api\\"):
        handle = self.open_file(link)
        self.write_value(intensity_word, contextual_neighborhood, word_central_neighborhood, handle)
        handle.close()
        self.llC_.pipe_log("The local API in json format was published, please find it in the folder: 'api_local' defined", "INFO", "api_local() : pipe_api_local()")

    def __init__(self):
        self.luC_ = luC.utils()
        self.llC_ = llC.log()
        self.date = datetime.datetime.now()
