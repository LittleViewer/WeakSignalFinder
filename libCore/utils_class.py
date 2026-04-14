import pathlib
import sys
import os
import datetime
import unicodedata

class utils :
    def check_file_exist(self, link):
        handle = pathlib.Path(self.absolute_link(link))
        return handle.exists()
    
    def error_with_reason(self, reason, to_break = False, code = 1000):
        print(f"[{self.date_}] - Stop Reason: " + reason)
        if to_break == True:
            sys.exit(code)

    def file_open(self, link, mode = "r", encoding_would="utf-8"):
        handle = open(os.path.abspath(self.absolute_link(link)), mode, encoding=encoding_would)
        return handle
    
    def create_dir(self, link, would_create = True) :
        if would_create == True:
            os.mkdir(self.absolute_link(link))
        return True
    
    def order_dict(self, items_add_dict, organiser_element, dict_orderized, tick ):
        if tick == 0 :
            dict_orderized[organiser_element] = [items_add_dict]
            return dict_orderized
        
        list_key = list(dict_orderized.keys())
        if organiser_element in list_key :
            dict_orderized[organiser_element].append(items_add_dict)
        else: 
             dict_orderized[organiser_element] = [items_add_dict]
        return dict_orderized
    
    def string_formated_name_file(self, string, unformated_sign = [".", ",",",","'",";", "?", "!",":","-", " ", "/","<",">",":",'"',"/","\\","|","?","*"]):
        string_formated = ""
        for one_sign in string:
            if one_sign in unformated_sign:
                string_formated = string_formated + "_"
            else:
                string_formated = string_formated + one_sign
        return string_formated
    
    def absolute_link(self, link):
            return os.path.abspath(link)+"\\"
    
    def remove_accent(self, text):
        if self.is_string(text) == False:
            self.error_with_reason("Is not string variable : remove_accent()", True)
        return "".join( c for c in unicodedata.normalize("NFD", text) if unicodedata.category(c) != "Mn")

    def is_string(self, possible_string):
        if type(possible_string) == str:
            return True
        return False
    
    def is_dict(self, possible_dict):
        if type(possible_dict) == dict:
            return True
        return False
    
    def __init__(self):
        self.date_ = datetime.datetime.now()