from ast import While
class utils_interaction_terminal:

    def create_list_number_by_list(self, list):
        dict_list_number = {}
        tick = 0
        for one_element in list:
            print(f"{tick} - {one_element}")
            dict_list_number[tick] = one_element
            tick += 1
        return dict_list_number

    def input_user_check(self, message, type_accept, data_accept):
        while True:
            choose_user = input(message)
            check = True
            if type_accept == int or type_accept == float:
                try :
                    choose_user = type_accept(choose_user)
                except:
                    print("This input is not interger like 1,2.. or float like 1.0,2.5.. Try again.")
                    check = False
                
                if check == True:
                    if choose_user not in set(data_accept.keys()):
                        print("This input not allow. Try again.")
                        check = False
                    else:
                        break
        return choose_user

    def __init__(self):
        pass