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
            print('envoi en cour...')
            server_mail = smtplib.SMTP(email_config_local.config_server,
                                       email_config_local.config_port)
            server_mail.starttls()
            server_mail.login(email_config_local.config_email, email_config_local.config_password)

            if isinstance(self.email_destidateur, (list, tuple)):
                to_addrs = self.email_destidateur
            else:
                to_addrs = [self.email_destidateur]

            email_body = f"Subject: Notification de transfert\n\n{self.message}"
            server_mail.sendmail(email_config_local.config_email, to_addrs, email_body)
            server_mail.quit()
            self.finished.emit()
        except Exception as e:
            self.error.emit(str(e))

    @staticmethod
    def envoi_email(email_destidateur, message):
        worker = Email_Worker(email_destidateur, message)
        worker.run()

