import routerClassPackage
import core_engine_pipe as ceP
import endpoint_user_pipe as euP
import sys

import libCore.config_tool_class as ctC;obj_class_router = routerClassPackage.routerFunctionPipe(ctC.config_toml_tool().key_return("parameter","start_file","global_program"))
silent_mode = False
obj_args = obj_class_router["argument_start"]().pipe_argument_start()
args = obj_args[0]
argument_run = obj_args[1]

licence_text = "\x1b]8;;https://github.com/LittleViewer/WeakSignalFinder?tab=License-1-ov-file\x1b\\Copyright (c) 2025-present LittleViewer & WeakSignalFinder Contributors\x1b]8;;\x1b\\"
print(fr"""
 _    _            _      _____ _                   _  ______ _           _           
| |  | |          | |    /  ___(_)                 | | |  ___(_)         | |          
| |  | | ___  __ _| | __ \ `--. _  __ _ _ __   __ _| | | |_   _ _ __   __| | ___ _ __ 
| |/\| |/ _ \/ _` | |/ /  `--. \ |/ _` | '_ \ / _` | | |  _| | | '_ \ / _` |/ _ \ '__|
\  /\  /  __/ (_| |   <  /\__/ / | (_| | | | | (_| | | | |   | | | | | (_| |  __/ |   
 \/  \/ \___|\__,_|_|\_\ \____/|_|\__, |_| |_|\__,_|_| \_|   |_|_| |_|\__,_|\___|_|   
                                   __/ |                                              
                                  |___/                                                                                                                 
    {licence_text.center(60)}""")


if args.install:
    print("[INFO] - You're session is not logged because the installation occurs in a degraded system situation!")
    obj_class_router["install_class"]().pipe_install()
    sys.exit()


try:
    obj_database = obj_class_router["prepare_request"]().connect_dabase()
    job_id = obj_class_router["log"]().pipe_jobId_session_generator(obj_database)
except Exception as e:
    print("Error with launch system : Please launch 'main.py --install'")
    sys.exit()

obj_class_router["log"]().pipe_log("Start execute program", "INFO","main")
def log_mode(mode):
    obj_class_router["log"]().pipe_log(f"Enter in the program mode : {mode}","INFO","main")


verbose = True
if args.silent_mode :
   verbose = False
obj_class_router["verbose_initialize"]().pipe_verbose_initialize(verbose)





if args.endpoint_user:
    log_mode("endpoint_user")
    euP.main(job_id)
elif args.engine_run:
    log_mode("engine_run")
    ceP.main(job_id)
else:
    print("Not argument provided")
    print(f"You can use : {argument_run}")

obj_class_router["log"]().pipe_log("Stop execute program", "INFO","main")

