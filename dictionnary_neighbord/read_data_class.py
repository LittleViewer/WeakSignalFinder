import routerClassPackage
import os
import json

class read_data :
    def prepare_sub_dict(self):
        handle_exclude = self.obj_class_router["utils"]().file_open(self.obj_class_router["utils"]().absolute_link(self.obj_class_router["config_toml_tool"]().key_return("path","exclude_file","read_data_dictionnary")))
        exclude_file = set(handle_exclude.read().split("\n"))

        path = self.obj_class_router["utils"]().absolute_link(self.obj_class_router["config_toml_tool"]().key_return("path","dataset","read_data_dictionnary"))
        all_file_name = os.listdir(f"{path}")
        already_read = self.obj_class_router["enter_data_dictionnary"](self.job_id).is_file_read()
        dict_path = []
        for one_file_name in all_file_name:
            if one_file_name not in exclude_file:
                if one_file_name not in already_read:
                    dict_path.append(self.obj_class_router["utils"]().absolute_link(f"{path}/{one_file_name}"))
        return dict_path
    
    def open_file(self, dict_all_path):
        all_data = []
        all_filename_read = []
        for one_path in dict_all_path:
            all_filename_read.append(str(one_path))
            with open(one_path, "r") as file:
                for line in file:
                    line = line.strip()
                    if line:
                        all_data.append(json.loads(line))
        self.obj_class_router["enter_data_dictionnary"](self.job_id).already_read(all_filename_read)
        return all_data             

    def read_data(self, all_data):
        dict_with_all_word = {}
        dict_with_word_intensity = {}
        list_all_word = set([])

        for one_block in all_data:
            dict_with_word_intensity = self.read_intensity_word(one_block, dict_with_word_intensity)
            one_block = json.loads(one_block[self.obj_class_router["config_toml_tool"]().key_return("parameter","part_of_local_api","for_launch")])
            for one_line in one_block:
                if one_line not in list_all_word :
                    list_all_word.add(one_line)
                    dict_with_all_word[one_line] = {"before" : [], "after" : []}

                for one_direction_word in one_block[one_line]:
                    list_new = one_block[one_line][one_direction_word]
                    list_old = dict_with_all_word[one_line][one_direction_word]
                    dict_with_all_word[one_line][one_direction_word] = set(list_new+list(list_old)) 
        return [dict_with_all_word, dict_with_word_intensity]

    def read_intensity_word(self, one_block, dict_saver):
        if len(json.loads(one_block["intensity_word"])) != 0:
            dict_saver[one_block["time_jobid"].strip("[]'")] = json.loads(one_block["intensity_word"])
        return dict_saver

    def pipe_read_data(self):
        all_path = self.prepare_sub_dict()
        all_data = self.open_file(all_path)
        return self.read_data(all_data)

    def __init__(self, job_id):
        import libCore.config_tool_class as ctC;self.obj_class_router = routerClassPackage.routerFunctionPipe(ctC.config_toml_tool().key_return("parameter","start_file","global_program"))
        self.job_id = job_id
