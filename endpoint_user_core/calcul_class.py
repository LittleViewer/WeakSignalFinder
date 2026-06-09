import endpoint_user_core.utils_interaction_terminal_class as uiC
import libCore.utils_class as luC
import libCore.config_tool_class as ctC
import libCore.log_class as llC
import datetime
import json
from numpy import average


class calcul_class:

    def check_word_exist(self, list_word):
        word_set = set(list_word)
        while True:
            word_choose = input("Please enter a word (e.g. word, sentence..) or 'w' to voir tous les mots: ")
            if word_choose.lower() == "w":
                self.uiC_.create_list_number_by_list(list_word)
                continue
            if word_choose not in word_set:
                print(f"'{word_choose}' not exist in list.")
                continue
            return word_choose

    def concentration_word_calcul(self, obj_db, prepare_request,name_calcul):
        list_date = []
        dict_multiple_intensity_run = {}
        obj_db[1].execute(prepare_request["completed_request"]["select_multiple_intensity_run"])
        all_run_multiple_intensity = obj_db[1].fetchall()
        for one_run in all_run_multiple_intensity:
            if one_run[1] not in set(list_date):
                dict_multiple_intensity_run[one_run[1]] = [one_run[0]]
                list_date.append(one_run[1])
            else:
                dict_multiple_intensity_run[one_run[1]].append(one_run[0])
        print("Please select date of run :")
        dict_list_number = self.uiC_.create_list_number_by_list(list_date)
        choose_date = self.uiC_.input_user_check("Choose (e.g: 0,1..) : ", int, dict_list_number)
        print(dict_list_number[choose_date])
        print(f"Please select a jobId from a run of the {dict_list_number[choose_date]} :")
        list_job_id = self.uiC_.create_list_number_by_list(dict_multiple_intensity_run[dict_list_number[choose_date]])
        choose_job_id = list_job_id[self.uiC_.input_user_check("Choose (e.g: 0,1..) : ", int, list_job_id)]

        obj_db[1].execute(prepare_request["template_request"]["select_with_where"].replace("table", "multiple_intensity_word").replace("column", "jobId").replace("value", "'"+choose_job_id+"'"))
        all_multiple_intensity_word = obj_db[1].fetchall()
        list_word = []
        dict_word_intensity = {}
        for one_multiple_intensity in all_multiple_intensity_word:
            list_word.append(one_multiple_intensity[1])
            dict_word_intensity[one_multiple_intensity[1]] = one_multiple_intensity[3] 

        
        choose_word = self.check_word_exist(list_word)
        absolute_multiple_value = float(dict_word_intensity[choose_word])
        
        obj_db[1].execute(prepare_request["template_request"]["select_word_with_where"].replace("word_replace", choose_word))
        all_word_multiple_intensity = obj_db[1].fetchall()
        all_calculate = []
        all_calcul = []
        all_line = {"concentration_value" : "concentration_value = word_frequency/word_with_total_frequency & deduplicate"}
        for one_word_multiple_intensity in all_word_multiple_intensity:
            result_sub = float(one_word_multiple_intensity[0])/absolute_multiple_value
            calcul_sub = f"{float(one_word_multiple_intensity[0])/absolute_multiple_value} = {one_word_multiple_intensity[0]}/{absolute_multiple_value}"
            all_calculate.append(result_sub)
            all_calcul.append(calcul_sub)
            all_line[result_sub] = calcul_sub
        calcul_for_result_point = f"salience_score({average(all_calculate)/len(all_calculate)}) = average(density({average(all_calculate)}))/number_corpus_word_in({len(all_calculate)})"
        result = f"The density of {choose_word} is Average : {average(all_calculate)} on {len(all_calculate)} input therefore obtains a score of {average(all_calculate)/len(all_calculate)}"
        print(result)
        output_data = {"global_result" :{"word" : choose_word, "result":result,"explicated_calcul" : calcul_for_result_point},"sub_result (one_line_per_one_value)":all_line}
        self.output_file(name_calcul,output_data)

    def output_file(self,name, list_dict_data, dir_path = "endpoint_user_core\\output"):
        if len(list_dict_data) == 0:
            print("No data for output!")
            return False
        type_file_accept = self.ctC_.key_return("parameter","type_output_file","endpoint_user")
        want_save_data = self.uiC_.create_list_number_by_list(["Yes","No"])
        accept_save = self.uiC_.input_user_check("Do you want to save the data? (e.g: 0,1..) : ", int, want_save_data)
        if accept_save == 0:
            list_purpose_choose = self.uiC_.create_list_number_by_list(type_file_accept)
            choose_user_type = self.uiC_.input_user_check("Choose file type (e.g: 0,1..) : ", int, list_purpose_choose)
            type_choose = list_purpose_choose[choose_user_type]
            prepare_name_file = f"{datetime.datetime.now().strftime('%y%m%d%H%M%S')}_{name}.{type_choose}"
            handle=self.luC_.file_open(self.luC_.absolute_link(f"{dir_path}\\{prepare_name_file}"),"a+")
            if type_choose == "json":
                json.dump(list_dict_data,handle,indent=4)
            elif type_choose == "txt":
                for one_title in list_dict_data:
                    handle.write(f"==={one_title}===\n")
                    sub_dict = list_dict_data[one_title]
                    for one_line in sub_dict:
                        handle.write("- ")
                        if len(str(one_line)) == 0:
                            handle.write("[Error: No Data]\n")
                        else:
                            handle.write(f"{one_line} : {sub_dict[one_line]}\n")
            handle.close()
            print(f"Successufly save data in {dir_path}\\{prepare_name_file}")
            self.llC_.pipe_log(f"Successufly save data in {dir_path}\\{prepare_name_file}","INFO","calcul_class() : output_file()")

    def __init__(self):
        self.uiC_ = uiC.utils_interaction_terminal()
        self.ctC_ = ctC.config_toml_tool()
        self.luC_ = luC.utils()
        self.llC_ = llC.log()
