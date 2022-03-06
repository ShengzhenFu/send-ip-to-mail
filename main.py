from apscheduler.scheduler import Scheduler
from sendmail import send_email_ssl_qq
from aliyunDdns import updateAllDns
import time

if __name__ == '__main__':
    
    sched = Scheduler()
    
    sched.add_interval_job(send_email_ssl_qq, hours=1, start_date='2021-06-29 07:30', args='')
    sched.add_interval_job(updateAllDns, hours=1, start_date='2021-06-29 07:30', args='')
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