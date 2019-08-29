#!/usr/bin/python

import smtplib

with open("pw.txt") as f:
    p = f.readline()
    print(p)

sender = "brunanayaramlima@gmail.com"
receiver = sender

server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
server.login(sender, p)
server.sendmail(
  sender, 
  receiver,
  "this message is from python")
server.quit()

