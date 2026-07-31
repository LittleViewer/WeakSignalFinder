import routerClassPackage
import datetime

class contextual_neighboord:

    def create_neigbhoor (self, block, neigbhoor_dict):
        for one_word_tick in range(len(block)):
            if len(block) == 1:
                return False
            else:
                if one_word_tick == 0:
                    neigbhoor_dict["before"].append([block[one_word_tick], block[one_word_tick+1]])
                elif one_word_tick == len(block)-1:
                    neigbhoor_dict["after"].append([block[one_word_tick-1],block[one_word_tick]])
                else:
                    neigbhoor_dict["beetween"].append([block[one_word_tick-1],block[one_word_tick], block[one_word_tick+1]])
        return neigbhoor_dict
    
    def number_total_neighboord(self, neighboord_multiple_dict):
        value = {}
        all = 0
        for one_index in neighboord_multiple_dict:
            value[one_index] = len(neighboord_multiple_dict[one_index])
            all = all + len(neighboord_multiple_dict[one_index])
        value["all"] = all
        return value

    def pipe_contextual_neighboord(self, data,obj_database,job_id):
        neighboord_multiple_dict = {"before" : [], "beetween" : [], "after" : []}
        for one_index in data:
            for one_block in data[one_index]:
               neighboord_multiple_dict = self.create_neigbhoor(one_block, neighboord_multiple_dict)
        stat_neighboord = self.number_total_neighboord(neighboord_multiple_dict)
        self.obj_class_router["cache_gestion"]().wrapper_add_data_in_file(job_id,f"Contextual Neighboord : {stat_neighboord['before']} before words central word, {stat_neighboord['after']} after words central word, and {stat_neighboord['beetween']} words before/after central words for {stat_neighboord['all']} neighboord word.",self.obj_class_router["config_toml_tool"]().key_return("filename","email_content","cache"))
        self.obj_class_router["log"]().save_data_set(neighboord_multiple_dict, stat_neighboord["all"],"contextual_neighboord")
        self.obj_class_router["prepare_request"]().insert_data_database(job_id, obj_database[0],obj_database[1],"saveData",["jobId","dateTime","type","data"],[[job_id,datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),"dataSetContextualNeighboords",str(neighboord_multiple_dict).replace("'",'"')]])
        self.obj_class_router["log"]().pipe_log(f"A dictionary of all semantic neighborhoods is created with {stat_neighboord['all']} neighboord.","INFO","contextual_neighboord() : pipe_contextual_neighboord()")
        return neighboord_multiple_dict

    def obtain_word(self, central_word, sentence, dictionnary_all_word):
        id_word_sentence = sentence.index(central_word)
        number_words_sentence = len(sentence)-1

        if number_words_sentence <= 1:
            return False

        if id_word_sentence == number_words_sentence:
            dictionnary_all_word[central_word]["before"].append(sentence[id_word_sentence-1])
            return dictionnary_all_word
        elif id_word_sentence == 0:
            dictionnary_all_word[central_word]["after"].append(sentence[id_word_sentence+1])
            return dictionnary_all_word
        else:
            dictionnary_all_word[central_word]["before"].append(sentence[id_word_sentence-1])
            dictionnary_all_word[central_word]["after"].append(sentence[id_word_sentence+1])
            return dictionnary_all_word
    
    def optimize_block_neighborhood(self, dictionnary_all_word):
        for one_central_word in dictionnary_all_word:
            for one_block in dictionnary_all_word[one_central_word]:
                dictionnary_all_word[one_central_word][one_block] = list(set(dictionnary_all_word[one_central_word][one_block]))
        return dictionnary_all_word

    def stat_dictonnary_all_word(self, dictionnary_all_word):
        before = 0
        after = 0
        for one_word in dictionnary_all_word :
            before += len(dictionnary_all_word[one_word]["before"])
            after += len(dictionnary_all_word[one_word]["after"])
        return {"number_central_words" : len(dictionnary_all_word), "number_before_word" : before,"number_after_word" : after }

    def pipe_neighborhood_center_on_word(self, contextual_neighboorhood_sentence,obj_database,job_id):
        all_word = []
        dictionnary_all_word = {}
        for one_index in contextual_neighboorhood_sentence:
            for one_sentence in contextual_neighboorhood_sentence[one_index]:
                for one_word in one_sentence:
                    if one_word not in set(all_word):
                        dictionnary_all_word[one_word] = {"before": [], "after": []}
                        all_word.append(one_word)
                        result = self.obtain_word(one_word, one_sentence, dictionnary_all_word)
                    else:
                        result = self.obtain_word(one_word, one_sentence, dictionnary_all_word)
                    if bool(result) != False:
                        dictionnary_all_word = result.copy()
        dictionnary_all_word = self.optimize_block_neighborhood(dictionnary_all_word)
        dict_stat = self.stat_dictonnary_all_word(dictionnary_all_word)
        self.obj_class_router["cache_gestion"]().wrapper_add_data_in_file(job_id,f"Contextual Neighboor Center on Central Word : {dict_stat['number_central_words']} central words with {dict_stat['number_before_word']} with words before and {dict_stat['number_after_word']} words after.",self.obj_class_router["config_toml_tool"]().key_return("filename","email_content","cache"))
        self.obj_class_router["log"]().save_data_set(dictionnary_all_word, len(dictionnary_all_word),"central_word_neighboord")
        self.obj_class_router["prepare_request"]().insert_data_database(job_id, obj_database[0],obj_database[1],"saveData",["jobId","dateTime","type","data"],[[job_id,datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),"dataSetcentralWordNeighboord",str(dictionnary_all_word).replace("'",'"')]])
        self.obj_class_router["log"]().pipe_log(f"A dictionary of semantic neighborhoods center in central word is created with {len(dictionnary_all_word)} neighboord.","INFO","contextual_neighboord() : pipe_neighborhood_center_on_word()")
        return dictionnary_all_word
        
    def __init__(self):
        import libCore.config_tool_class as ctC;self.obj_class_router = routerClassPackage.routerFunctionPipe(ctC.config_toml_tool().key_return("parameter","start_file","global_program"))