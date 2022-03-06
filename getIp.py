# !/usr/bin/env python
# -*- coding:utf-8 -*-
import requests
import re
import subprocess
import time
import os
from common import Log
import urllib.request

logger = Log()

def cmd_reset_wifi(delay):
    # for windows ONLY
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
    return str(lst[0])

def get_my_publick_ip():
    get_ip_method = os.popen('curl -s myip.ipip.net')
    get_ip_responses = get_ip_method.readlines()[0]
    get_ip_pattern = re.compile(r'\d+\.\d+\.\d+\.\d+')
    get_ip_value = get_ip_pattern.findall(get_ip_responses)
    return get_ip_value

# 获取外网地址
def get_internet_ip():
    with urllib.request.urlopen('http://www.3322.org/dyndns/getip') as response:
        html = response.read()
        ip = str(html, encoding='utf-8').replace("\n", "")
    return ip
