import endpoint_user_core.interaction_user_class as iuC
import routerClassPackage


def main(job_id):
    print("Enter in the Weak Signal Finder - Endpoint User Mode!")    
    
    import libCore.config_tool_class as ctC; routerClassPackage.routerFunctionPipe(ctC.config_toml_tool().key_return("parameter","start_file","global_program"))["interaction_user"](job_id).central_menu()