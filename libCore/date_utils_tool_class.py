import routerClassPackage
import datetime

class date_utils_tool:
    def grab_db_date(self, obj_db ,table):
        obj_db[1].execute(f"SELECT * FROM {table} ORDER BY date_ DESC LIMIT 1;")
        return obj_db[1].fetchall()[0][1].split("-")

    def is_ready_date_to_run(self, obj_db ,table, name_parameter):
        date_db = self.grab_db_date(obj_db, table)
        date_old = datetime.datetime(int(date_db[0]),int(date_db[1]),int(date_db[2]))
        date_now_complete = datetime.datetime.now()
            
        diff_date = date_now_complete - date_old
        if diff_date.days >= self.obj_class_router["config_toml_tool"]().key_return("parameter",name_parameter,"for_launch"):
            return True
        else :
            return False

    def enter_last_run(self, obj_database, table,job_id):
        obj_database[1].execute(f"INSERT INTO {table} VALUES ('{job_id}','{self.date_today}');")
        obj_database[0].commit()

    def time_delta_list(self, days_int):
        array_old_date = [str(self.date_today)]
        is_int = self.obj_class_router["utils"]().is_type(int, days_int)
        if is_int == False:
            self.obj_class_router["utils"]().error_with_reason(f"[{datetime.datetime.now()}] - This variable is not interger!",False)
            self.obj_class_router["log"]().pipe_log("This variable is not integer!","WARN","date_utils_tool() : time_delta_list()")
            return False
        for one_day in range(days_int):
            array_old_date.append(str(self.date_today - datetime.timedelta(days=(one_day+1))))
        return array_old_date

    def __init__(self):
        import libCore.config_tool_class as ctC;self.obj_class_router = routerClassPackage.routerFunctionPipe(ctC.config_toml_tool().key_return("parameter","start_file","global_program"))
        self.date_today = datetime.date.today()