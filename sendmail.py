# !/usr/bin/env python
# -*- coding:utf-8 -*-
 
import smtplib, ssl
from email.message import EmailMessage
from getIp import getIp
import time, datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from apscheduler.scheduler import Scheduler
from settings import OUTLOOK_USER, OUTLOOK_PWD, RECEIVERS, SENDER

from ipCompare import ipChanged, saveIp
from common import Log


logger = Log()


def send_email_ssl():
    # content
    current_time = datetime.datetime.now()
    sender = "shengzhen.fu@outlook.com"
    reciever = "fushengzhen@163.com"
    password = "junglescout@2021"
    msg_body = 'Home IP is ' + getIp() + ', checking time: '+ str(current_time)
            
    # action
    msg = EmailMessage()
    msg['subject'] = 'Email sent using outlook.'   
    msg['from'] = sender
    msg['to'] = reciever
    msg.set_content(msg_body)
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp-mail.outlook.com', 465, context=context) as smtp:
        smtp.login(sender, sender,password)
        smtp.ehlo()
        print('smtp server working fine')
        time.sleep(5)
        smtp.send_message(msg)
        smtp.quit()

def send_email_starttls():
    # set up the SMTP server
    if ipChanged() == True:
        print("detect IP change, will send email")
        logger.info("detect IP change, will send email")
        s = smtplib.SMTP(host='smtp-mail.outlook.com', port=587)
        s.starttls()
        s.login(OUTLOOK_USER, OUTLOOK_PWD)
        s.ehlo()
        print ('smtp server connection is good')
        logger.info('smtp server connection is good')
        time.sleep(2)
        sender = SENDER
        current_time = datetime.datetime.now()
        receivers = [RECEIVERS]
        text = "my home IP address is " + getIp() + ", checking time: " + str(current_time)
        msg = MIMEMultipart('alternative')
        content = MIMEText(text, 'plain')
        msg['Subject']='Home IP check'
        msg['From']=SENDER
        msg['To']=RECEIVERS
        msg.attach(content)
        s.sendmail(sender, receivers, msg.as_string())
        print ('sent email via outlook at: '+time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        logger.info('sent email to '+ str(receivers)+ '  at: ' + str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))) )
        s.quit()
        saveIp()
    elif ipChanged() == False:
        print("ip not changed, will not send out email")
        logger.info("ip not changed, will not send out email")


if __name__ == '__main__':
    
    sched = Scheduler()
    
    sched.add_interval_job(send_email_starttls, hours=1, start_date='2021-06-10 23:30', args='')
    # # https://apscheduler.readthedocs.io/en/v2.1.2/cronschedule.html
    # #sched.add_cron_job(send_email_starttls, month='6-8,11-12', day_of_week='mon-fri', hour='9-19')
    sched.start()
    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        print('exit')
        sched.shutdown() 

