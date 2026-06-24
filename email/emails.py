import smtplib 
import email_config 


class Email:
    @staticmethod
    def envoi_email(email_destinataire, message):
        server_mail = smtplib.SMTP(email_config.config_server, email_config.config_port)
        server_mail.starttls()
        server_mail.login(email_config.config_email, email_config.config_password)
        server_mail.sendmail(email_config.config_email, email_destinataire, message)
        server_mail.quit()


message = "message à envoyer"

if __name__ == '__main__':
    
    Email.envoi_email("exem@gmail.com", message)


