import smtplib 
from . import email_config_local
from PySide6.QtCore import QObject, Signal, Slot

class Email_Worker(QObject):
    finished = Signal()
    error = Signal(str)

    def __init__(self, email_destidateur, message):
        super().__init__()
        self.email_destidateur = email_destidateur
        self.message = message

    @Slot()
    def run(self):
        try:
            print('envoi en cours')
            server_mail = smtplib.SMTP(email_config_local.config_server,
                                       email_config_local.config_port)
            server_mail.starttls()
            server_mail.login(email_config_local.config_email, email_config_local.config_password)
            server_mail.sendmail(email_config_local.config_email,self.email_destidateur)
            server_mail.quit()
            self.finished.emit()
        except Exception as e:
            self.error.emit(str(e))

