import libCore.config_tool_class as ctC
import argparse

class argument_start :
    def pipe_argument_start(self):
        argument_run = self.ctC_.key_return("parameter","argument_run","global_program")
        for one_argument in argument_run:
            self.parser.add_argument(one_argument, action="store_true")
        args = self.parser.parse_args()
        return [args,argument_run]
    
    def __init__(self):
        self.ctC_ = ctC.config_toml_tool()
        self.parser = argparse.ArgumentParser()