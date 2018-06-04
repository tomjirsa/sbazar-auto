import smtplib
from email.mime.text  import MIMEText


msg = MIMEText("... telo emailu ...")
msg['subject'] = 'Nejaky titulek'
msg['from'] = 'from'
msg['To'] = 'to'
s = smtplib.SMTP_SSL('smtp.seznam.cz:465') #587 je port, muze byt 25 nebo tak neco

login = input("Your Login: ")
password = input("Passwond: ")

s.login(login, password)

s.sendmail(login,['tom.jirsik@gmail.com'], msg.as_string())
s.quit()