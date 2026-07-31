import routerClassPackage

class cache_gestion:
    def pipe_create_cache_file(self, job_id_, name_cache_file = "_unknow_", path_dir = "libCore\\cache_service_wsf\\"):
            formated_path =  self.obj_class_router["utils"]().absolute_link(path_dir)
            if self.obj_class_router["utils"]().check_file_exist(path_dir) == False:
                self.obj_class_router["utils"]().create_dir(formated_path)
            if name_cache_file == "_unknow_" or len(name_cache_file) <= 1:
                self.obj_class_router["log"]().pipe_log("Not specify name of cache file!","ERROR","cache_gestion() : pipe_create_cache_file()")
                self.obj_class_router["utils"]().error_with_reason("Not specify name of cache file : cache_gestion() : create_cache_file()")
                return False
            else :
                handle_file = self.obj_class_router["utils"]().file_open(self.obj_class_router["utils"]().absolute_link(f"{path_dir}{job_id_}_{name_cache_file}.cache.wsf"),"a+")
                handle_file.write(f"{self.initial_message}\n")
                handle_file.close()
    
    def pipe_add_data_content_file(self, job_id, content, name_cache_file = "_unknow_", path_dir = "libCore\\cache_service_wsf\\"):
        path = self.obj_class_router["utils"]().absolute_link(f"{path_dir}{job_id}_{name_cache_file}.cache.wsf")
        if name_cache_file == "_unknow_" or self.obj_class_router["utils"]().check_file_exist(path) == False :
            self.obj_class_router["log"]().pipe_log("Wrong filename!","ERROR","cache_gestion() : pipe_add_data_content_file()")
            self.obj_class_router["utils"]().error_with_reason("Wrong filename : cache_gestion() : pipe_add_data_content_file()")
            return False
        handle_file = self.obj_class_router["utils"]().file_open(path,"a+")
        accept_ = True
        if type(content) != str:
            accept_ == False
        if len(content) <= 1:
            accept_ = False
        if accept_ == False:
            self.obj_class_router["log"]().pipe_log("Pleaser enter content for add string in cache file!","ERROR","cache_gestion() : pipe_add_data_content_file()")
            self.obj_class_router["utils"]().error_with_reason("Pleaser enter content for add string in cache file : cache_gestion() : pipe_add_data_content_file()")
            handle_file.close()
            return False
            
        handle_file.write(f"{content}\n")
        handle_file.close()

    def wrapper_add_data_in_file(self, job_id, content, name_file):
        if self.obj_class_router["config_toml_tool"]().key_return("parameter","authorize_run","email_auto") == True :
            self.obj_class_router["cache_gestion"]().pipe_add_data_content_file(job_id, content,name_file)

    def get_content_cache_file(self,job_id,name_cache_file,path_dir = "libCore\\cache_service_wsf\\"):
        path = self.obj_class_router["utils"]().absolute_link(f"{path_dir}{job_id}_{name_cache_file}.cache.wsf")
        if self.obj_class_router["utils"]().check_file_exist(path) == False :
            self.obj_class_router["log"]().pipe_log("Wrong filename!","ERROR","cache_gestion() : get_content_cache_file()")
            return False
        handle_file = self.obj_class_router["utils"]().file_open(path)
        content = handle_file.read()
        handle_file.close()
        content_array = content.splitlines()
        for one_lines in content_array:
            if one_lines != self.initial_message:
                content_array.pop(0)
                break
        return content_array


    def __init__(self):
        self.initial_message = "===initialize cache files==="
        import libCore.config_tool_class as ctC;self.obj_class_router = routerClassPackage.routerFunctionPipe(ctC.config_toml_tool().key_return("parameter","start_file","global_program"))