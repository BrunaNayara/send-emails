# Import smtplib for the actual sending function
# https://docs.python.org/3/library/smtplib.html
import smtplib

# Import the email modules we'll need
# https://docs.python.org/3.4/library/email-examples.html
from email.mime.text import MIMEText

from bs4 import BeautifulSoup

##### Beautiful Soup methods
# Get email template
def get_template(template_file):
    with open(template_file) as fp:
        template = BeautifulSoup(fp, 'html.parser')

    return template

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


##### Email and mime methods
# create mail message
def create_mail(subject, body, sender):
    msg = MIMEText(body, 'html')
    msg['Subject'] = subject
    msg['From'] = sender

    return msg

# create custom mail (change greetings)
def create_custom_mail(subject, body, receiver, sender):
    soup = custom_greeting(receiver['name'], body)

    subject = receiver['name'] + ", " + subject

    msg = create_mail(subject, soup, sender)

    return msg

def change_receiver(receiver, msg):
    #receiver{ name: "str", email: "email@mail.com"}
    del msg['To']
    msg['To'] = receiver['email']

    return msg

##### SMTP methods
# send email
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

##### Send functions
def send_to_list(mail_list, msg):
    for receiver in mail_list:
        send_to_one(receiver, msg)

def send_to_one(receiver, msg):
    msg = change_receiver(receiver, msg)
    send(msg)

def prepare_message(template_file, sender):
    soup = get_template(template_file)
    soup = change_sender_name(sender, soup)
    mail = create_mail("subject", soup)

    return mail


def main():
    tf = "email_template.html"
    me = "Bruna"
    mail = prepare_message(tf, me)

    r1 = {'name':"Bruna", 'email':"aaaaa@gmail.com" }
    r2 = {'name':"Brenda", 'email':"aaaaa@gmail.com" }
    r3 = {'name':"Matheus", 'email':"aaaaaa@gmail.com" }
    maillist = [r1, r2, r3]

    print("send one")
    send_to_one(r1, mail)
    print("send list")
    send_to_list(maillist, mail)


def send_custom_mails():
    tf = "email_template.html"
    me = "Bruna"
    subject = "Assunto personalizado"

    r1 = {'name':"Bruna", 'email':"aaaaaa@gmail.com" }
    r2 = {'name':"Brenda", 'email':"aaaaa@gmail.com" }
    r3 = {'name':"Matheus", 'email':"aaaaaaa@gmail.com" }
    maillist = [r1, r2, r3]

    body = get_template(tf)

    for receiver in maillist:
        mail = create_custom_mail(subject, body, receiver, me)
        send_to_one(receiver, mail)



def main():
    # TODO change main to send custom mail to the list

    # send_same_email()
    send_custom_mails()



if __name__ == "__main__":
    main()




##### unused
def send_my_email(msg):
    soup = get_template(template_file)
    receiver = {'name':receiver_name, 'email':receiver_email }


    soup = custom_greeting(receiver['name'], soup)
    soup = change_sender_name(sender_name, soup)


    mail = create_mail("Olá, esse é um email", soup)
    mail = change_receiver(mail, receiver)

    send(mail)
# send_my_email("email_template.html", "Bruna", "Matheus", "aaaaa@gmail.com")



