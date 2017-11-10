#!/usr/bin/env python
# -*- coding:utf-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.header import Header


def send_email(mail_host, mail_user, mail_pwd, to_addrs, subject, content):
    msg = MIMEText(content, _charset='utf-8')
    msg['Subject'] = Header(subject, 'utf-8')
    msg['From'] = mail_user

    smtp = smtplib.SMTP_SSL(mail_host, 465)
    # smtp.set_debuglevel(1)
    smtp.login(mail_user, mail_pwd)
    smtp.sendmail(mail_user, to_addrs, msg.as_string())
    smtp.quit()
