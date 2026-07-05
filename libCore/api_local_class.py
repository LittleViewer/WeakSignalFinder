import routerClassPackage
import datetime
import json

class api_local:
    
    def open_file(self, link):
        handle = self.obj_class_router["utils"]().file_open(self.obj_class_router["utils"]().absolute_link(link)/f"{self.date.year}_{self.date.month}_{self.date.day}.local_api.txt","a+")
        return handle

    def write_value(self, job_id, intensity_word, contextual_neighborhood, word_central_neighborhood, handle):
        content_api = json.dumps({"time" : f"[{self.date}]", "time_jobid" : f"[{job_id}]", "intensity_word" : intensity_word, "contextual_neighborhood" : contextual_neighborhood, "word_central_neighborhood" : word_central_neighborhood})+"\n"
        handle.write(content_api)
    
    def pipe_api_local(self, obj_database,job_id):
        dict_data_type = {}
        api_brut = self.obj_class_router["prepare_request"]().get_data_table_where_like(obj_database[0],"saveData","jobId",job_id)
        for one_obj in range(len(api_brut)):
            dict_data_type[api_brut[one_obj][2]] = api_brut[one_obj][3]
        handle = self.open_file(self.obj_class_router["config_toml_tool"]().key_return("path","open_file","api_local"))
        self.write_value(job_id, dict_data_type["saveStateWordIntensity"], dict_data_type["dataSetContextualNeighboords"], dict_data_type["dataSetcentralWordNeighboord"], handle)
        handle.close()
        self.obj_class_router["log"]().pipe_log("The local API in json format was published, please find it in the folder: 'api_local' defined", "INFO", "api_local() : pipe_api_local()")

    def __init__(self):
        import libCore.config_tool_class as ctC;self.obj_class_router = routerClassPackage.routerFunctionPipe(ctC.config_toml_tool().key_return("parameter","start_file","global_program"))
        self.date = datetime.datetime.now()
        
