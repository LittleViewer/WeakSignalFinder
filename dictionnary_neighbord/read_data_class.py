import libCore.config_tool_class as ctC
import libCore.utils_class as luC
import dictionnary_neighbord.enter_data_dictionnary_class as edC
import os
import json

class read_data :
    def prepare_sub_dict(self):
        handle_exclude = self.luC_.file_open(self.luC_.absolute_link(self.ctC_.key_return("path","exclude_file","read_data_dictionnary")))
        exclude_file = set(handle_exclude.read().split("\n"))

        path = self.luC_.absolute_link(self.ctC_.key_return("path","dataset","read_data_dictionnary"))
        all_file_name = os.listdir(f"{path}")
        already_read = self.edC_.is_file_read()
        dict_path = []
        for one_file_name in all_file_name:
            if one_file_name not in already_read:
                if one_file_name not in exclude_file:
                    dict_path.append(self.luC_.absolute_link(f"{path}/{one_file_name}"))

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
        self.edC_.already_read(all_filename_read)
        return all_data             

    def read_data(self, all_data):
        dict_with_all_word = {}
        list_all_word = set([])

        for one_block in all_data:
            one_block = json.loads(one_block["word_central_neighborhood"])

            for one_line in one_block:
                if one_line not in list_all_word :
                    list_all_word.add(one_line)
                    dict_with_all_word[one_line] = {"before" : [], "after" : []}

                for one_direction_word in one_block[one_line]:
                    list_new = one_block[one_line][one_direction_word]
                    list_old = dict_with_all_word[one_line][one_direction_word]
                    dict_with_all_word[one_line][one_direction_word] = set(list_new+list(list_old)) 

        return dict_with_all_word

    def pipe_read_data(self):
        all_path = self.prepare_sub_dict()
        all_data = self.open_file(all_path)
        return self.read_data(all_data)

    def __init__(self, job_id):
        self.ctC_ = ctC.config_toml_tool()
        self.luC_ = luC.utils()
        self.edC_ = edC.enter_data_dictionnary(job_id)