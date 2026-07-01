import core_engine_pipe as ceP
import endpoint_user_pipe as euP
import install.install_pipe_class as ipC
import database_rss_run.prepare_request_class as prC
import libCore.argument_start_class as asC
import libCore.log_class as llC
import verbose_initialize_wsf as viW
import sys

asC_ = asC.argument_start()
viW_ = viW.verbose_initialize()
ipC_ = ipC.install_class()

silent_mode = False
obj_args = asC_.pipe_argument_start()
args = obj_args[0]
argument_run = obj_args[1]
llC_ = llC.log()

prC_ = prC.prepare_request()
licence_text = "\x1b]8;;https://github.com/LittleViewer/WeakSignalFinder?tab=License-1-ov-file\x1b\\Copyright (c) 2025-present LittleViewer & WeakSignalFinder Contributors\x1b]8;;\x1b\\"
print(f"""
 _    _            _      _____ _                   _  ______ _           _           
| |  | |          | |    /  ___(_)                 | | |  ___(_)         | |          
| |  | | ___  __ _| | __ \ `--. _  __ _ _ __   __ _| | | |_   _ _ __   __| | ___ _ __ 
| |/\| |/ _ \/ _` | |/ /  `--. \ |/ _` | '_ \ / _` | | |  _| | | '_ \ / _` |/ _ \ '__|
\  /\  /  __/ (_| |   <  /\__/ / | (_| | | | | (_| | | | |   | | | | | (_| |  __/ |   
 \/  \/ \___|\__,_|_|\_\ \____/|_|\__, |_| |_|\__,_|_| \_|   |_|_| |_|\__,_|\___|_|   
                                   __/ |                                              
                                  |___/                                                                                                                 
    {licence_text.center(60)}\n""")


if args.install:
    print("[INFO] - You're session is not logged because the installation occurs in a degraded system situation!")
    ipC_.pipe_install()
    sys.exit()


try:
    obj_database = prC_.connect_dabase()
    job_id = llC_.pipe_jobId_session_generator(obj_database)
except Exception as e:
    print("Error with launch system : Please launch 'main.py --install'")
    sys.exit()

llC_.pipe_log("Start execute program", "INFO","main")
def log_mode(mode):
    llC_.pipe_log(f"Enter in the program mode : {mode}","INFO","main")


verbose = True
if args.silent_mode :
   verbose = False
viW_.pipe_verbose_initialize(verbose)





if args.endpoint_user:
    log_mode("endpoint_user")
    euP.main(job_id)
elif args.engine_run:
    log_mode("engine_run")
    ceP.main(job_id)
else:
    print("Not argument provided")
    print(f"You can use : {argument_run}")

llC_.pipe_log("Stop execute program", "INFO","main")

