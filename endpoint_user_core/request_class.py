import routerClassPackage

class request_class:

    def find_by_pattern(self):
        while True:
            number_word = 0
            pattern_user = input("Enter the word (e.g: w,wa,war..) : ").lower()
            self.obj_db[1].execute(self.prepare_request["template_request"]["find_word_by_pattern"].replace("pattern",pattern_user))
            result_pattern = self.obj_db[1].fetchall()
            print(self.prepare_request["template_request"]["find_word_by_pattern"].replace("pattern",pattern_user))
            if len(result_pattern) != 0:
                list_word = list(set([one_word[0] for one_word in result_pattern]))
                number_word = len(list_word)
                for one_word in list_word:
                    print(f"- {one_word}")
                print(f"Your search to find {number_word} words.")
            else :
                print(f"No word for {pattern_user}.")
            
            
            response = self.obj_class_router["utils_interaction_terminal"]().pipe_question_for_user(["continue","return"])
            if response == "return":
                return False
            else:
                print(f"Your old search : {pattern_user} for {number_word} words.")

        

    def __init__(self, obj_db, prepare_request):
        import libCore.config_tool_class as ctC;self.obj_class_router = routerClassPackage.routerFunctionPipe(ctC.config_toml_tool().key_return("parameter","start_file","global_program"))
        self.obj_db = obj_db
        self.prepare_request = prepare_request