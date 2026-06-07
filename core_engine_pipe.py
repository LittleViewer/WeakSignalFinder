import libCore.feed_class as lfC
import libCore.prepare_data_class as lpC
import libCore.log_class as llC
import libCore.utils_class as luC
import libCore.config_tool_class as ctC
import libCore.frequency_one_word_class as fowC
import libCore.contextual_neighborhood_class as cnC
import libCore.api_local_class as alC
import libCore.email_smtp_class as esC
import libCore.date_utils_tool_class as dtC
import database_rss_run.prepare_request_class as prC
import dictionnary_neighbord.read_data_class as rdC
import dictionnary_neighbord.enter_data_dictionnary_class as edC
import dictionnary_neighbord.intensity_db_word_engine_class as idweC

import asyncio
import datetime
import gc

def main(job_id):
    lfC_ = lfC.feed()
    llC_ = llC.log()
    luC_ = luC.utils()
    lpC_ = lpC.prepare_data()
    fowC_ = fowC.frequency_one_word()
    cnC_ = cnC.contextual_neighboord()
    alC_ = alC.api_local()
    esC_ = esC.email_smtp()
    dtC_ = dtC.date_utils_tool()
    prC_ = prC.prepare_request()
    ctC_ = ctC.config_toml_tool()


    obj_database = prC_.connect_dabase()

    print(f"[{datetime.datetime.now()}] Start execute program!")
    all_article = asyncio.run(lfC_.pipe_extract_rss())
    data_clean_for_analyse = lpC_.pipe_prepare_data(all_article,obj_database,job_id)
    intensity_word = fowC_.pipe_frequency_one_word(data_clean_for_analyse,obj_database,job_id)
    contextual_neighborhood = neighboord_multiple_dict = cnC_.pipe_contextual_neighboord(data_clean_for_analyse,obj_database,job_id)
    word_central_neighborhood = cnC_.pipe_neighborhood_center_on_word(neighboord_multiple_dict,obj_database,job_id)
    alC_.pipe_api_local(obj_database,"'"+job_id+"'")

    del all_article,data_clean_for_analyse,intensity_word,contextual_neighborhood,word_central_neighborhood,obj_database
    gc.collect()
    
    rdC_ = rdC.read_data(job_id)
    edC_ = edC.enter_data_dictionnary(job_id)

    obj_database_dictionnary = edC_.connect_dabase()
    idweC_ = idweC.intensity_db_word_engine_class(obj_database_dictionnary)

    date_time = datetime.datetime.now()
    got_to_launch = dtC_.is_ready_date_to_run(obj_database_dictionnary, "run", "cooldown_day_launch_dictionnary")
    if got_to_launch == True:
        llC_.pipe_log(f"A run to complete the dictionary has just been automatically launched!","INFO","main")
        prepared_data = rdC_.pipe_read_data()
        edC_.pipe_enter_data(prepared_data[0])
        if ctC_.key_return("parameter","authorize_run_intensity_engine","for_launch") == True:
            idweC_.pipe_main_engine(prepared_data[1],job_id)
        dtC_.enter_last_run(obj_database_dictionnary,"run",job_id)
        llC_.pipe_log(f"The dictionary completion run is over!","INFO","main")

    esC_.sub_smtp_send(f"Weak Signal Finder is finished! \nTime : {date_time}\n Job ID : {job_id}\n Link Github Repository : https://github.com/LittleViewer/WeakSignalFinder\n Copyright (c) 2025-present LittleViewer & WeakSignalFinder Contributors",f"Subject: Weak Signal Finder Notification : Execution completed successfully - {job_id} !")

    print(f"[{date_time}] Stop execute program!")
