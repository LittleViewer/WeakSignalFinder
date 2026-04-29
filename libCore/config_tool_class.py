import libCore.utils_class as luC
import tomllib

class config_toml_tool:

    def key_return(self, table,key, sub_table = None):
        if self.luC_.is_string(table) != True or self.luC_.is_string(key) != True:
            self.luC_.error_with_reason("An error occurred with the configuration file!")
            return False
        if sub_table == None:
            return self.config[table][key]
        else:
            if self.luC_.is_string(sub_table) != True:
                self.luC_.error_with_reason("An error occurred with the configuration file!")
                return False
            return self.config[table][sub_table][key]

    def __init__(self, path = "input_configuration\\external_configuration.toml"):
        self.luC_ = luC.utils()
        handle = open(self.luC_.absolute_link("config_weakSignalFinder.toml"),"rb")
        self.config = tomllib.load(handle)
