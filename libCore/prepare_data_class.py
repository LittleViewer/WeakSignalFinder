import libCore.utils_class as luC
import libCore.log_class as llC
import database.prepare_request_class as prC
import spacy
import json
import datetime
import re

class prepare_data:

    def scrap_util_data(self, data_brut, index_lang, dict_data_clean):
        for one_index_article in data_brut:
           dict_data_clean[index_lang].append([" ".join(one_index_article[0].split()), " ".join(one_index_article[1].split())])
        return dict_data_clean

    def extract_possible_word(self, structured_data):
        all_article_with_possible_word = {}
        for one_index in structured_data:
            all_article_with_possible_word[one_index] = []
            for one_article in structured_data[one_index]:
                for index_article in range(len(one_article)):
                    one_bloc = []
                    for one_word in re.sub(r'[^a-z0-9\u00C0-\u017E ]', ' ', self.luC_.remove_accent(one_article[index_article]).lower()).split(" "):
                        if re.sub(r'[^a-z0-9]', '', one_word) and len(one_word) >= 3:
                            one_bloc.append(one_word)
                if len(one_bloc) >= 1:
                    all_article_with_possible_word[one_index].append(one_bloc)
        return all_article_with_possible_word
    
    def prepare_file_essential_word(self, link_model = "libCore\\input\\languageModel.json", link_stop_word = "libCore\\input\\stopword.txt"):
        data_file = []
        tick = 0
        try :
            for one_link in [link_model, link_stop_word]:
                handle_file =  self.luC_.file_open(self.luC_.absolute_link(one_link))
                if tick == 0:
                    data_file.append(json.loads(handle_file.read()))
                else:
                    data_file.append(handle_file.read().split("\n"))
                tick += 1
        except:
            self.llC_.pipe_log("The files could not be read.", "CRITICAL", "prepare_data() : prepare_file_essential_word()")
            self.luC_.error_with_reason("The files could not be read : prepare_file_essential_word()", True)
        return data_file

    def remove_no_essential_word(self, structured_data_sub_clean, id_model, new_dict):
        list_type_word_accept = set(["NOUN", "PROPN", "VERB", "ADJ"])
        list_model_id_support = []
        list_model_name_support = {}
        list_file_util = self.prepare_file_essential_word()
        stop_word_set = set(list_file_util[1])
        for one_model in list_file_util[0]:
            list_model_id_support.append(one_model["code_language"])
            list_model_name_support[one_model["code_language"]] = one_model["model_name"]
        list_model_set = set(list_model_id_support)
        if id_model not in list_model_set:
            self.llC_.pipe_log(f"A model is not present in the database, the id : {id_model}", "prepare_data() : remove_no_essential_word()", "WARN")
            return False     
        new_dict[id_model] = []
        nlp = spacy.load(list_model_name_support[id_model])
        for one_block in structured_data_sub_clean[id_model]:
            new_block = []
            for one_word in one_block :
                one_word = nlp(one_word)
                one_word_lemma = one_word[0].lemma_
                if one_word_lemma not in stop_word_set :
                    if one_word[0].pos_ in list_type_word_accept:
                        new_block.append(one_word_lemma)
            new_dict[id_model].append(new_block)
        return new_dict
            

    def pipe_prepare_data(self,data_brut,obj_database,job_id):
        structured_data_sub_clean = {}
        if self.luC_.is_dict(data_brut) == False:
            self.llC_.pipe_log("Input variable is not dict: prepare_data() : pipe_prepare_data()","CRITICAL","pipe_prepare_data()")
            self.luC_.error_with_reason("Input variable is not dict: pipe_prepare_data()", True) 

        for one_index_lang in data_brut:
            structured_data_sub_clean[one_index_lang] = []
            structured_data_brut = self.scrap_util_data(data_brut[one_index_lang], one_index_lang, structured_data_sub_clean)

        structured_data_sub_clean = self.extract_possible_word(structured_data_brut)
        self.llC_.save_state(structured_data_sub_clean,"Brut")
        self.prC_.insert_data_database(obj_database[0],obj_database[1],"saveData",["jobId","dateTime","type","data"],[[job_id,datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),"saveStateBrut",str(structured_data_sub_clean).replace("'",'"')]])

        structured_data_clean_ = {}
        for one_index_lang in structured_data_brut:
            structured_data_clean_ = self.remove_no_essential_word(structured_data_sub_clean, one_index_lang, structured_data_clean_)
        self.llC_.save_state(structured_data_clean_,"Clean")
        self.prC_.insert_data_database(obj_database[0],obj_database[1],"saveData",["jobId","dateTime","type","data"],[[job_id,datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),"saveStateClean",str(structured_data_clean_).replace("'",'"')]])


        return structured_data_clean_



    def __init__(self):
        self.luC_ = luC.utils()
        self.llC_ = llC.log()
        self.prC_ = prC.prepare_request()