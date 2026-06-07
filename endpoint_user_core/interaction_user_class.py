from ast import While
import libCore.log_class as llC
import libCore.config_tool_class as ctC
import libCore.utils_class as luC
import dictionnary_neighbord.enter_data_dictionnary_class as edC
import endpoint_user_core.calcul_class as ecC_
import endpoint_user_core.utils_interaction_terminal_class as uitC_
import datetime
import json

class interaction_user:


    def open_prepare_request(self, file_link = "endpoint_user_core\\template\\prepared_request.json"):
        handle = self.luC_.file_open(self.luC_.absolute_link(file_link))
        return json.loads(handle.read())

    def central_menu(self):
        dict_sub_menu = self.ctC_.key_return("parameter","initial_menu","endpoint_user")
        dict_double_pair = {}
        print("Main Menu :")
        tick = 0
        for one_sub_menu in dict_sub_menu:
            print(f"{tick} - {one_sub_menu}")
            dict_double_pair[tick] = one_sub_menu
            tick += 1
        response_user = input("Choose (e.g: 0,1..) : ")
        try :
            choose_value = dict_sub_menu[dict_double_pair[int(response_user)]]
        except :
            self.llC_.pipe_log(f"Invalid value : {response_user}","ERROR","interaction_user() : central_menu()")
            self.central_menu()
            return False
        
        self.llC_.pipe_log(f"User in Main Menu choose value : {choose_value}","INFO","interaction_user() : central_menu()")
        if self.ctC_.key_return("parameter","authorize_exit","endpoint_user") == choose_value:
            self.exit_parameter()
        elif self.ctC_.key_return("parameter","authorize_about","endpoint_user") == choose_value:
            self.about_parameter()
        elif self.ctC_.key_return("parameter","authorize_calcul","endpoint_user") == choose_value:
            self.calcul_parameter()
        elif self.ctC_.key_return("parameter","authorize_help","endpoint_user") == choose_value:
            self.help_parameter()
        else:
            self.central_menu()
        
    def help_parameter(self, link = "endpoint_user_core\\template\\help_prepared.json"):
        print("Help Parameter :")
        handle = self.luC_.file_open(self.luC_.absolute_link(link))
        dict_help = json.load(handle)
        list_accept = self.uitC_.create_list_number_by_list(dict_help.keys())
        choose_accept = self.uitC_.input_user_check("Choose (e.g: 0,1..) : ", int, list_accept)
        sub_help = dict_help[list_accept[choose_accept]]
        sub_list_accept = self.uitC_.create_list_number_by_list(dict_help[list_accept[choose_accept]].keys())
        sub_choose_accept = self.uitC_.input_user_check("Choose (e.g: 0,1..) : ", int, sub_list_accept)
        result = sub_list_accept[sub_choose_accept]
        self.llC_.pipe_log(f"The user reads the help for {result} in {list_accept[choose_accept]}.","INFO","interaction_user() : help_parameter()")
        print(sub_help[result])
        self.last_sub_menu()

    def calcul_parameter(self):
        print("Calcul Parameter :")
        list_calcul = self.ctC_.key_return("parameter","list_calcul","endpoint_user")
        list_accept = self.uitC_.create_list_number_by_list(list_calcul.keys())
        choose_accept = self.uitC_.input_user_check("Choose (e.g: 0,1..) : ", int, list_accept)
        self.llC_.pipe_log(f"The user requests the calculation of {list_accept[choose_accept]}.","INFO","interaction_user() : choose_accept()")
        if choose_accept == 0:
            self.ecC_.concentration_word_calcul(self.obj_db, self.prepare_request)
        else:
            print(choose_accept)
        self.last_sub_menu()

    def about_parameter(self):
        print(f"""
        Weak Signal Finder

        Date : {datetime.datetime.today().date()}
        Time : {str(datetime.datetime.today().time()).split(".")[0]}
        Job Id of this Session : {self.job_id}
        Licence : MIT
        Credit : Copyright (c) 2025-present LittleViewer & WeakSignalFinder Contributors
        Repo Link : https://github.com/LittleViewer/WeakSignalFinder
        """)
        self.last_sub_menu()


    def exit_parameter(self):
        print("Program is Finished!")
        self.llC_.pipe_log("User exit the program","INFO","interaction_user() : exit_parameter()")
        return False

    def last_sub_menu(self):
        choose = input("Exit (E) or Main Menu (M): ").lower()
        self.llC_.pipe_log(f"User in last sub menu choose value : {choose}","INFO","interaction_user() : last_sub_menu()")
        if choose == "e" or choose == "exit":
            return self.exit_parameter()
        elif choose == "m" or choose == "main menu"  or choose == "main" or choose == "menu":
            return self.central_menu()
        else:
            self.last_sub_menu()

    def __init__(self, job_id):
        self.ctC_ = ctC.config_toml_tool()
        self.edC_ = edC.enter_data_dictionnary(job_id)
        self.luC_ = luC.utils()
        self.obj_db = self.edC_.connect_dabase()
        self.prepare_request = self.open_prepare_request()
        self.job_id = job_id
        self.llC_ = llC.log()
        self.llC_.insert_job_id(job_id)
        self.ecC_ = ecC_.calcul_class()
        self.uitC_ = uitC_.utils_interaction_terminal()