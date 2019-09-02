# Import smtplib for the actual sending function
# https://docs.python.org/3/library/smtplib.html
import smtplib

# Import the email modules we'll need
# https://docs.python.org/3.4/library/email-examples.html
from email.mime.text import MIMEText

# Import Beautiful Soup to parse html
from bs4 import BeautifulSoup

# Import getpass
import getpass

# Import csv reader
import csv

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

# Change custom word
def change_secret_word(word, template):
    greetings = template.select_one("#secret-word")
    greetings.string = "{}".format(word)

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
    soup = change_secret_word(receiver['word'], body)

    subject = receiver['name'] + ", " + subject

    msg = create_mail(subject, soup, sender)

    return msg

def change_receiver(receiver, msg):
    #receiver{ name: "str", email: "email@mail.com"}
    del msg['To']
    msg['To'] = receiver['email']

    return msg

##### SMTP methods
def get_pass():
    return getpass.getpass(prompt='Password:')


# send email
def send(msg):
    # get sender mail from file
    with open("mail.txt") as f:
        me = f.readline()

    # get password from file
    with open("pw.txt") as f:
        p = f.readline()

    # get using getpass
    # p = get_pass()

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(me, p)
    server.send_message(msg)
    server.quit()

##### Send functions
def send_to_list(mail_list, msg):
    for receiver in mail_list:
        send_to_one(receiver, msg)

def send_to_one(receiver, msg):
    print("sending to " + receiver['name'])
    msg = change_receiver(receiver, msg)
    send(msg)

def prepare_message(template_file, sender, subject):
    soup = get_template(template_file)
    soup = change_sender_name(sender, soup)
    mail = create_mail(subject, soup, sender)

    return mail

##### CSV functions
def get_maillist_from_csv(csv_file):
    maillist = []
    with open(csv_file, newline='') as csvfile:
        c = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in c:
            m = dict([('name', row[0]), ('email', row[1]), ('word', row[2])])
            maillist.append(m)
            print(row[0])

    return maillist

##### Example fucntions

def send_same_email(maillist):
    tf = "email_template.html"
    me = "Bruna"
    subject = "Esse é o assunto"


    print("send one")
    send_to_one(r1, mail)
    print("send list")
    send_to_list(maillist, mail)


def send_custom_mails(maillist):
    tf = "email_template.html"
    me = "Bruna"
    subject = "Assunto personalizado"


    body = get_template(tf)

    for receiver in maillist:
        mail = create_custom_mail(subject, body, receiver, me)

        send_to_one(receiver, mail)



def main():
    # TODO change main to send custom mail to the list

    csv_file = 'maillist.csv'
    maillist = get_maillist_from_csv(csv_file)

    # send_same_email(maillist)
    send_custom_mails(maillist)



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



