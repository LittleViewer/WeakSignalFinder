import libCore.utils_class as luC
import sqlite3
import sys

class prepare_request:

    def connect_dabase(self, link_to_database):
        try :
            if self.luC_.is_string(link_to_database) == True:
                handle_dabase = sqlite3.connect(self.luC_.absolute_link(link_to_database))
                cursor_database = handle_dabase.cursor()
            else :
                self.luC_.error_with_reason("The expected formats are not provided as input in prepare_request.connect_dabase()!",True)
        except:
            self.luC_.error_with_reason("An unexpected error occurs during the connection with the database in prepare_request.connect_dabase()!",True)
        return [cursor_database,handle_dabase]

    
    def get_data_table(self, cursor, table_name):
        if self.luC_.is_string(table_name) == False:
            self.luC_.error_with_reason("The expected formats are not provided as input in prepare_request.get_data_table_where_like()!",True)
        cursor.execute(f"SELECT * FROM {table_name}")
        return cursor.fetchall()
    
    def get_data_table_where_like(self, cursor, table_name, column_name, like_value):
        if self.luC_.is_string(table_name) == False or self.luC_.is_string(column_name) == False or self.luC_.is_string(like_value) == False:
            self.luC_.error_with_reason("The expected formats are not provided as input in prepare_request.get_all_data_table()!",True)
        cursor.execute(f"SELECT * FROM {table_name} WHERE {column_name} LIKE {like_value};")
        return cursor.fetchall()
        
    def is_data_already_insert(self, cursor, table_name, value):
        all_data_in_table = self.get_data_table(cursor, table_name)
        for one_row in all_data_in_table:
            if type(one_row) == tuple:
                one_row = list(one_row)
            if value == one_row:
                return True
        return False

    def insert_data_database(self, cursor, handle_database, table_name, column_name, values):
        if self.luC_.is_string(table_name) != True or self.luC_.is_list(column_name) != True:
            self.luC_.error_with_reason("The expected formats are not provided as input in prepare_request.insert_data_database()#32!",True)
        temp_values = []
        for one_array in values:
            sub_temp_values = []
            for one_value in one_array:
                if self.is_data_already_insert(cursor, table_name, one_value) == False:
                    sub_temp_values.append(one_value)
                else:
                    sub_temp_values.append("NULL")
            temp_values.append(sub_temp_values)
        values = temp_values
        if len(values) == 0:
            return False

        prepare_request = f"INSERT INTO {table_name} ("
        tick_all_column = len(column_name)
        
        for one_column in range(tick_all_column):
            if one_column == tick_all_column-1:
                prepare_request = prepare_request+f"{column_name[one_column]}) VALUES "  
            else:
                prepare_request = prepare_request+f"{column_name[one_column]},"
        
        tick_values_all_row = len(values)
        for one_row_values in range(tick_values_all_row):
            one_row_content = values[one_row_values]
            
            if self.luC_.is_list(one_row_content) != True:
                self.luC_.error_with_reason("The expected formats are not provided as input in prepare_request.insert_data_database()#57!",True)
            tick_all_one_row = len(values[one_row_values])
            prepare_one_row_insert = "("

            for one_id_values in range(tick_all_one_row):    
                if one_id_values == tick_all_one_row-1:
                    prepare_one_row_insert = prepare_one_row_insert +"'"+ one_row_content[one_id_values]+"')"
                else:
                    prepare_one_row_insert = prepare_one_row_insert +"'"+ one_row_content[one_id_values]+"',"
                
            if tick_values_all_row-1 == one_row_values:
                prepare_request = prepare_request + prepare_one_row_insert + ";"
            else :
                prepare_request = prepare_request + prepare_one_row_insert + ","
        try :
            cursor.execute(prepare_request)
            handle_database.commit()
        except Exception as error:
            if sqlite3.IntegrityError == type(error):
                self.luC_.error_with_reason("There is an error with an integrity constraint, such that data already entered is entered again!")
            else:
                self.luC_.error_with_reason("An unexpected error occurred while inserting data into the database!",True)
        
    def delete_data(self, cursor, handle_database, table_name, column_name, data):
        try:
            if self.luC_.is_string(table_name) != True or self.luC_.is_string(column_name) != True or self.luC_.is_string(data) != True:
                self.luC_.error_with_reason("The expected formats are not provided as input in prepare_request.delete_data()!",True)
            prepare_request = f"DELETE FROM {table_name} WHERE {column_name} LIKE '{data}';"
            cursor.execute(prepare_request)
            handle_database.commit()
        except:
            self.luC_.error_with_reason("An unexpected error occurs when trying to delete data!",True)

    def __init__(self):
        self.luC_ = luC.utils()