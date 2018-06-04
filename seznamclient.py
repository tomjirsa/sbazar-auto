import smtplib
from email.mime.text  import MIMEText

class Seznam_email:
    def __init__(self):
        self.login = ""
        self.passwd = ""
        self.connection = ""

    def getCredentials(self):
        self.login = input("Your Login: ")
        self.passwd = input("Passwond: ")

    def connect(self):
        self.connection = smtplib.SMTP_SSL('smtp.seznam.cz:465')
        self.connection.login(self.login,self.passwd)

    def sendEmail(self, message_text, recepient):
        msg = MIMEText(message_text)
        msg["subject"] = 'Sbazar watchdog'
        msg["from"] = self.login
        msg["To"] = recepient
        try:
            self.connection.sendmail(self.login, [recepient], msg.as_string())

        except:
            print("Can not send email.")

    def disconnect(self):
        self.connection.quit()
