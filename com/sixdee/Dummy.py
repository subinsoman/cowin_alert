import smtplib

gmail_user = 'tosubins@gmail.com'
gmail_password = 'trzmfrlxmppsufbo'

sent_from = 'vaccinealert@gmail.com'
to = ['subin.soman@6dtech.co.in']
cc = []
bcc = []
subject = 'OMG Super Important Message Vaccine '
body = 'Hey Dude, '
to = [to] + cc + bcc
message = 'Subject: {}\n\n{}'.format(subject, body)
try:
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(gmail_user, gmail_password)
    server.sendmail(sent_from, to, message)
    server.close()
except Exception as e:
    # Print any error messages to stdout
    print(str(e))