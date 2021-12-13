import os
import smtplib
from email.message import EmailMessage

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


class MailConfig:
    EMAIL = os.environ.get('EMAIL')
    PASSWORD = os.environ.get('PASSWORD')
    HOST = os.environ.get('HOST')
    PORT = int(os.environ.get('PORT'))

    def create_email_message(self):
        message = EmailMessage()
        message['From'] = self.EMAIL
        message['To'] = 'solohybdanylo@gmail.com'
        return message

    def connect_to_smtp_server_and_send_msg(self, msg):
        try:
            server = smtplib.SMTP(self.HOST, self.PORT)
            server.ehlo()
            server.starttls()
            server.login(self.EMAIL, self.PASSWORD)
            server.send_message(msg)
            server.close()
        except Exception as e:
            print(f'Error: {e}')
