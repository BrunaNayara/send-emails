# Import smtplib for the actual sending function
# https://docs.python.org/3/library/smtplib.html
import smtplib

# Import the email modules we'll need
# https://docs.python.org/3.4/library/email-examples.html
from email.mime.text import MIMEText

from bs4 import BeautifulSoup

# Get email template
def get_template(template):
    with open(template) as fp:
        soup = BeautifulSoup(fp, 'html.parser')

    return soup

# Greetings human
def custom_greeting(name, template):
    greetings = template.select_one("#greetings")
    greetings.string = "Olá, {}".format(name)

    return template


# Change made by
def change_sender_name(sender, template):
    greetings = template.select_one("#sender")
    greetings.string = "{}".format(sender)

    return template


# create mail message
def create_mail(subject, body):
    msg = MIMEText(body, 'html')
    msg['Subject'] = subject
    msg['From'] = "brunanayaramlima@gmail.com"

    return msg

def change_receiver(msg, receiver):
    #receiver{ name: "str", email: "email@mail.com"}
    msg['To'] = receiver['email']

    return msg

def send(msg):

    # get sender mail from file
    with open("mail.txt") as f:
        me = f.readline()

    # get password from file
    with open("pw.txt") as f:
        p = f.readline()

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(me, p)
    server.send_message(msg)
    server.quit()

def send_my_email(template_file, sender_name, receiver_name, receiver_email):
    soup = get_template(template_file)
    receiver = {'name':receiver_name, 'email':receiver_email }


    soup = custom_greeting(receiver['name'], soup)
    soup = change_sender_name(sender_name, soup)


    mail = create_mail("Olá, esse é um email", soup)
    mail = change_receiver(mail, receiver)

    send(mail)



send_my_email("email_template.html", "Bruna", "Matheus", "brunanayaramlima@gmail.com")

