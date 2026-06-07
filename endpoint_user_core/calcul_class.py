import endpoint_user_core.utils_interaction_terminal_class as uiC
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

    def concentration_word_calcul(self, obj_db, prepare_request):
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
        for one_word_multiple_intensity in all_word_multiple_intensity:
            all_calculate.append(float(one_word_multiple_intensity[0])/absolute_multiple_value)
            all_calcul.append(f"{float(one_word_multiple_intensity[0])/absolute_multiple_value} = {one_word_multiple_intensity[0]}/{absolute_multiple_value}")
        print(f"The density of {choose_word} is Average : {average(all_calculate)} on {len(all_calculate)} input therefore obtains a score of {average(all_calculate)/len(all_calculate)}")


    def __init__(self):
        self.uiC_ = uiC.utils_interaction_terminal()