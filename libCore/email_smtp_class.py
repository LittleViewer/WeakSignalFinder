import libCore.config_tool_class as ctC
import libCore.log_class as llC
import smtplib
import dotenv
import os

class email_smtp:
    def prepa_email(self, message, topic, list_part = ["sender","receiver","password_file","port","server"]):
        dict_email = {"message":message,"topic":topic}
        for one_part in list_part:
            dict_email[one_part] = self.ctC_.key_return("parameter",one_part,"email_auto")
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
        if self.ctC_.key_return("parameter","authorize_run","email_auto") == False:
            return False

        try:
            dict_email = self.prepa_email(message, topic)
        except Exception as e:
            self.llC_.pipe_log(f"Email not prepared", "ERROR","email_smtp")
            return False
        try:
            self.send_email(dict_email)
            self.llC_.pipe_log(f"Email sent to {dict_email['receiver']} with topic {dict_email['topic']}", "INFO","email_smtp")
        except Exception as e:
            self.llC_.pipe_log(f"Email not sent to {dict_email['receiver']} with topic {dict_email['topic']}", "ERROR","email_smtp")

    def __init__(self):
        self.ctC_ = ctC.config_toml_tool()
        self.llC_ = llC.log()