import routerClassPackage
import smtplib
import dotenv
import os

class email_smtp:
    def prepa_email(self, message, topic, list_part = ["sender","receiver","password_file","port","server"]):
        dict_email = {"message":message,"topic":topic}
        for one_part in list_part:
            dict_email[one_part] = self.obj_class_router["config_toml_tool"]().key_return("parameter",one_part,"email_auto")
        return dict_email

    def send_email(self, dict_email):
        dotenv.load_dotenv(dict_email["password_file"])
        with smtplib.SMTP(dict_email["server"], dict_email["port"]) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(dict_email["sender"], os.getenv("PASSWORD_EMAIL"))
            server.sendmail(dict_email["sender"], dict_email["receiver"], dict_email["topic"] + "\n" + dict_email["message"])

    def sub_smtp_send(self, message = "No body text.", topic = "No topic."):
        if self.obj_class_router["config_toml_tool"]().key_return("parameter","authorize_run","email_auto") == False:
            return False

        try:
            dict_email = self.prepa_email(message, topic)
        except Exception as e:
            self.obj_class_router["utils"]().error_with_reason(f"Email not prepared", False)
            return False
        try:
            self.send_email(dict_email)
        except Exception as e:
            self.obj_class_router["utils"]().error_with_reason(f"Email not sent to {dict_email['receiver']} with topic {dict_email['topic']}", False)

    def __init__(self):
        import libCore.config_tool_class as ctC;self.obj_class_router = routerClassPackage.routerFunctionPipe(ctC.config_toml_tool().key_return("parameter","start_file","global_program"))