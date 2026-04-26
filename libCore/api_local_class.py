import libCore.utils_class as luC
import libCore.log_class as llC
import database.prepare_request_class as prC
import datetime
import json

class api_local:
    
    def open_file(self, link):
        handle = self.luC_.file_open(self.luC_.absolute_link(link)/f"{self.date.year}_{self.date.month}_{self.date.day}.local_api.txt","a+")
        return handle

    def write_value(self, job_id, intensity_word, contextual_neighborhood, word_central_neighborhood, handle):
        content_api = json.dumps({"time" : f"[{self.date}]", "time_jobid" : f"[{job_id}]", "intensity_word" : intensity_word, "contextual_neighborhood" : contextual_neighborhood, "word_central_neighborhood" : word_central_neighborhood})+"\n"
        handle.write(content_api)
    
    def pipe_api_local(self, obj_database,job_id, link = "local_api\\"):
        dict_data_type = {}
        api_brut = self.prC_.get_data_table_where_like(obj_database[0],"saveData","jobId",job_id)
        for one_obj in range(len(api_brut)):
            dict_data_type[api_brut[one_obj][2]] = api_brut[one_obj][3]
        handle = self.open_file(link)
        self.write_value(job_id, dict_data_type["saveStateWordIntensity"], dict_data_type["dataSetContextualNeighboords"], dict_data_type["dataSetcentralWordNeighboord"], handle)
        handle.close()
        self.llC_.pipe_log("The local API in json format was published, please find it in the folder: 'api_local' defined", "INFO", "api_local() : pipe_api_local()")

    def __init__(self):
        self.luC_ = luC.utils()
        self.llC_ = llC.log()
        self.date = datetime.datetime.now()
        self.prC_ = prC.prepare_request()