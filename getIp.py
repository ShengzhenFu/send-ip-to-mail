# !/usr/bin/env python
# -*- coding:utf-8 -*-
import requests
import re
import subprocess
import time
from common import Log

logger = Log()

def cmd_reset_wifi(delay):
    # cmd = 'cmd.exe D:/code/send-ip-to-mail-py/reset_wifi.bat'
    p = subprocess.Popen("cmd.exe /c" + "D:/code/send-ip-to-mail-py/reset_wifi.bat", stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    curline = p.stdout.readline()
    while (curline != b''):
        print(curline)
        curline = p.stdout.readline()
    p.wait()
    print("wifi reset completed, "+str(p.returncode))
    logger.info("wifi reset completed, "+str(p.returncode))
    time.sleep(delay)


def getIp():
    # cmd_reset_wifi(10)
    URL = "https://myip.ipip.net"

    resp = requests.get(url = URL)
    ips = str(resp.content)
    pattern = re.compile((r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'))
    lst=[]
    for ip in ips:
        lst.append(pattern.search(ips)[0])
    #print(str(lst[0]))
    #resp.close()
    return str(lst[0])