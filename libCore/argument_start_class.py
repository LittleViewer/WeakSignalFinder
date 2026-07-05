import routerClassPackage
import argparse

class argument_start :
    def pipe_argument_start(self):
        argument_run = self.obj_class_router["config_toml_tool"]().key_return("parameter","argument_run","global_program")
        for one_argument in argument_run:
            self.parser.add_argument(one_argument, action="store_true")
        args = self.parser.parse_args()
        return [args,argument_run]
    
    def __init__(self):
        import libCore.config_tool_class as ctC;self.obj_class_router = routerClassPackage.routerFunctionPipe(ctC.config_toml_tool().key_return("parameter","start_file","global_program"))
        self.parser = argparse.ArgumentParser()