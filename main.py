import core_engine_pipe as ceP
import endpoint_user_pipe as euP
import database_rss_run.prepare_request_class as prC
import libCore.argument_start_class as asC
import libCore.log_class as llC
import verbose_initialize_wsf as viW

asC_ = asC.argument_start()
viW_ = viW.verbose_initialize()

silent_mode = False
obj_args = asC_.pipe_argument_start()
args = obj_args[0]
argument_run = obj_args[1]

verbose = True
if args.silent_mode :
   verbose = False
viW_.pipe_verbose_initialize(verbose)

llC_ = llC.log()
prC_ = prC.prepare_request()

llC_.pipe_log("Start execute program", "INFO","main")
obj_database = prC_.connect_dabase()
job_id = llC_.pipe_jobId_session_generator(obj_database)
def log_mode(mode):
    llC_.pipe_log(f"Enter in the program mode : {mode}","INFO","main")


if args.endpoint_user:
    log_mode("endpoint_user")
    euP.main(job_id)
elif args.install:
    log_mode("install")
elif args.engine_run:
    log_mode("engine_run")
    ceP.main(job_id)
else:
    print("Not argument provided")
    print(f"You can use : {argument_run}")

llC_.pipe_log("Stop execute program", "INFO","main")

