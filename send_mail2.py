# Import smtplib for the actual sending function
# https://docs.python.org/3/library/smtplib.html
import smtplib

# Import the email modules we'll need
# https://docs.python.org/3.4/library/email-examples.html
from email.mime.text import MIMEText

# Open a plain text file for reading.  For this example, assume that
# the text file contains only ASCII characters.
textfile = "email_template.html"
with open(textfile) as fp:
    # Create a html message
    msg = MIMEText(fp.read(), 'html')

# get password from file
with open("mail.txt") as f:
    me = f.readline()

you = me + "matheus.sousa.faria@gmail.com, "+ "brendanatalia94@gmail.com"

# me == the sender's email address
# you == the recipient's email address
msg['Subject'] = 'The contents of %s' % textfile
msg['From'] = me
msg['To'] = you

# get password from file
with open("pw.txt") as f:
    p = f.readline()

server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
server.login(me, p)
server.send_message(msg)
server.quit()
