import routerClassPackage

import asyncio
import datetime
import gc

def main(job_id):
    import libCore.config_tool_class as ctC;obj_class_router = routerClassPackage.routerFunctionPipe(ctC.config_toml_tool().key_return("parameter","start_file","global_program"))
    obj_database = obj_class_router["prepare_request"]().connect_dabase()

    print(f"[{datetime.datetime.now()}] Start execute program!")
    all_article = asyncio.run(obj_class_router["feed"]().pipe_extract_rss())
    data_clean_for_analyse = obj_class_router["prepare_data"]().pipe_prepare_data(all_article,obj_database,job_id)
    intensity_word = obj_class_router["frequency_one_word"]().pipe_frequency_one_word(data_clean_for_analyse,obj_database,job_id)
    contextual_neighborhood = neighboord_multiple_dict = obj_class_router["contextual_neighboord"]().pipe_contextual_neighboord(data_clean_for_analyse,obj_database,job_id)
    word_central_neighborhood = obj_class_router["contextual_neighboord"]().pipe_neighborhood_center_on_word(neighboord_multiple_dict,obj_database,job_id)
    obj_class_router["api_local"]().pipe_api_local(obj_database,"'"+job_id+"'")

    del all_article,data_clean_for_analyse,intensity_word,contextual_neighborhood,word_central_neighborhood,obj_database
    gc.collect()
    

    obj_database_dictionnary = obj_class_router["enter_data_dictionnary"](job_id).connect_dabase()

    date_time = datetime.datetime.now()
    got_to_launch = obj_class_router["date_utils_tool"]().is_ready_date_to_run(obj_database_dictionnary, "run", "cooldown_day_launch_dictionnary")
    if got_to_launch == True:
        obj_class_router["log"]().pipe_log(f"A run to complete the dictionary has just been automatically launched!","INFO","main")
        prepared_data = obj_class_router["read_data"](job_id).pipe_read_data()
        obj_class_router["enter_data_dictionnary"](job_id).pipe_enter_data(prepared_data[0])
        if obj_class_router["config_toml_tool"]().key_return("parameter","authorize_run_intensity_engine","for_launch") == True:
            obj_class_router["intensity_db_word_engine_class"](obj_database_dictionnary).pipe_main_engine(prepared_data[1],job_id)
        obj_class_router["date_utils_tool"]().enter_last_run(obj_database_dictionnary,"run",job_id)
        obj_class_router["log"]().pipe_log(f"The dictionary completion run is over!","INFO","main")

    obj_class_router["email_smtp"]().sub_smtp_send(f"Weak Signal Finder is finished! \nTime : {date_time}\n Job ID : {job_id}\n Link Github Repository : https://github.com/LittleViewer/WeakSignalFinder\n Copyright (c) 2025-present LittleViewer & WeakSignalFinder Contributors",f"Subject: Weak Signal Finder Notification : Execution completed successfully - {job_id} !")
    print(f"[{date_time}] Stop execute program!")
