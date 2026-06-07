import endpoint_user_core.interaction_user_class as iuC

def main(job_id):
    print("Welcom in the Weak Signal Finder - Endpoint User Mode!")

    iuC_ = iuC.interaction_user(job_id)
    
    iuC_.central_menu()