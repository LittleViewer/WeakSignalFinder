import libCore.utils_class as luC
import libCore.log_class as llC
import json

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

    def pipe_contextual_neighboord(self, data):
        neighboord_multiple_dict = {"before" : [], "beetween" : [], "after" : []}
        for one_index in data:
            for one_block in data[one_index]:
               neighboord_multiple_dict = self.create_neigbhoor(one_block, neighboord_multiple_dict)
        stat_neighboord = self.number_total_neighboord(neighboord_multiple_dict)
        self.llC_.save_data_set(neighboord_multiple_dict, stat_neighboord["all"],"contextual_neighboord")
        self.llC_.pipe_log(f"A dictionary of all semantic neighborhoods is created with {stat_neighboord['all']} neighboord.","INFO","contextual_neighboord() : pipe_contextual_neighboord()")
        return neighboord_multiple_dict

    def obtain_word(self, central_word, sentence, dictionnary_all_word):
        id_word_sentence = sentence.index(central_word)
        number_words_sentence = len(sentence)-1

        if number_words_sentence <= 1:
            return False
        if id_word_sentence == number_words_sentence:
            dictionnary_all_word[central_word]["before"].append(sentence[id_word_sentence-1])
        elif id_word_sentence == 0:
            dictionnary_all_word[central_word]["after"].append(sentence[id_word_sentence+1])
        else:
            dictionnary_all_word[central_word]["before"].append(sentence[id_word_sentence-1])
            dictionnary_all_word[central_word]["after"].append(sentence[id_word_sentence+1])
        return dictionnary_all_word
    
    def optimize_block_neighborhood(self, dictionnary_all_word):
        for one_central_word in dictionnary_all_word:
            for one_block in dictionnary_all_word[one_central_word]:
                dictionnary_all_word[one_central_word][one_block] = list(set(dictionnary_all_word[one_central_word][one_block]))
        return dictionnary_all_word

    def pipe_neighborhood_center_on_word(self, contextual_neighboorhood_sentence):
        all_word = []
        dictionnary_all_word = {}
        template_word_list = {"before" : [], "after" : []}
        for one_index in contextual_neighboorhood_sentence:
            for one_sentence in contextual_neighboorhood_sentence[one_index]:
                for one_word in one_sentence:
                    if one_word not in set(all_word):
                        dictionnary_all_word[one_word] = template_word_list
                        all_word.append(one_word)
                        result = self.obtain_word(one_word, one_sentence, dictionnary_all_word)
                    else:
                        result = self.obtain_word(one_word, one_sentence, dictionnary_all_word)
                    if bool(result) != False:
                        dictionnary_all_word = result.copy()
        dictionnary_all_word = self.optimize_block_neighborhood(dictionnary_all_word)
        self.llC_.save_data_set(dictionnary_all_word, len(dictionnary_all_word),"central_word_neighboord")
        self.llC_.pipe_log(f"A dictionary of semantic neighborhoods center in central word is created with {len(dictionnary_all_word)} neighboord.","INFO","contextual_neighboord() : pipe_neighborhood_center_on_word()")
        return dictionnary_all_word

       
        
    def __init__(self):
        self.luC_ = luC.utils()
        self.llC_ = llC.log()