from common import Log
from getIp import getIp


logger = Log()
def readIPfromCache():
    with open('cache-ip.txt', 'r') as f:
        str_cache = f.read()
        logger.info("read cache: " + str_cache)
        print("read cache: " + str_cache)
        if str_cache is not None:
            return str_cache
        else :
            return None

def saveIp():
    with open('cache-ip.txt', 'w') as f:
        f.write(getIp())
        print()
        logger.info('saved current IP '+getIp()+' to cache')

def ipChanged():
    cached_ip = readIPfromCache()
    current_ip = getIp()
    if cached_ip is not None:
        if current_ip == cached_ip :
            print("ip not changed")
            logger.info("ip not changed")
            return False
        if current_ip != cached_ip:
            logger.info("current IP is "+current_ip+" detect IP change")
            print("current IP is "+current_ip+" detect IP change")
            return True
    else:
        print("cached ip is empty, please check")
        logger.info("cached ip is empty, please check")
