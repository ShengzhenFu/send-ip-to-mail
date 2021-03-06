#coding=utf-8
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkalidns.request.v20150109.AddDomainRecordRequest import AddDomainRecordRequest
from aliyunsdkalidns.request.v20150109.DescribeDomainRecordsRequest import DescribeDomainRecordsRequest
from aliyunsdkalidns.request.v20150109.UpdateDomainRecordRequest import UpdateDomainRecordRequest
from aliyunsdkalidns.request.v20150109.DescribeDomainRecordInfoRequest import DescribeDomainRecordInfoRequest
from settings import accessKeyId, accessSecret, domainName
import json
import subprocess
import platform
from getIp import get_internet_ip
from common import Log

logger = Log()
rc_format = 'json'
dns_domain = domainName

"""
identify OS type
OS	                 Value
Linux (2.x and 3.x)	'Linux2'
Windows	            'Win32'
Windows/Cygwin	    'Cygwin'
Mac OS X	        'Darwin'
OS/2	            'Os2'
OS/2 EMX	        'Os2emx'
RiscOS	            'Riscos'
RiscOS	            'Riscos'
AtheOS	            'Atheos'
"""
def typeOfOS():
    plat_tuple=platform.architecture()
    system=platform.system()
    plat_version=platform.platform()
    # print(f'A {plat_tuple[0]} - {system} - version {plat_version}')
    if system == 'Darwin':
        print(f'this is a {plat_tuple[0]} Mac OS X system, version: {plat_version}')
        logger.info(f'this is a {plat_tuple[0]} Mac OS X system, version: {plat_version}')
        return 'Mac'
        
    elif system == 'Linux':
        print(f'this is a {plat_tuple[0]}  Linux system \n version: {plat_version}')
        logger.info(f'this is a {plat_tuple[0]}  Linux system \n version: {plat_version}')
        return 'Linux'

    elif system == 'Win32':
        print(f'this is a {plat_tuple[0]} Windows system \n version: {plat_version}')
        logger.info(f'this is a {plat_tuple[0]} Windows system \n version: {plat_version}')
        return 'Windows'
        
"""
run shell
"""
def runShell(cmd_shell):
    CompletedProcessObject=subprocess.run(args=cmd_shell,shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,universal_newlines=True,timeout=10,check=False)
    if CompletedProcessObject:
           code,out,err=CompletedProcessObject.returncode,CompletedProcessObject.stdout,CompletedProcessObject.stderr
    output = str.strip(out)
    error = str.strip(err)
    return code, output, error

"""
disConnect VPN
"""
def disconnectVpn():
    # currently support Mac OS X Monterey
    if typeOfOS() == 'Mac':
        str_shell="lsof '/Applications/ExpressVPN.app/Contents/MacOS/ExpressVPN' | awk 'NR==2{print $2}'"
        results = runShell(str_shell)
        code = results[0]
        output = results[1]
        error = results[2]
        print(f'code {code}, out {output}, err {error}')
        if code ==0:
            if output:
                kill_shell="kill "+output
                runKill = subprocess.Popen(kill_shell, shell=True)
                runKill.wait()
                print(f'vpn process has been ended with status {runKill.returncode}')
                logger.info(f'vpn process has been ended with status {runKill.returncode}')
                return output
            if error:
                logger.error(error)
                return error
        else:
            if code ==1:
                logger.error("????????????????????????")
            else:
                #logger.info(code)
                raise subprocess.CalledProcessError(code,str_shell)
    else: print("sorry, we don't support your OS yet, please use Mac OS X" )
    # TODO: support Linux and Windows

"""
???????????????????????????
"""
def checkRecords(dns_domain):
    clt = AcsClient(accessKeyId, accessSecret, 'cn-hangzhou')
    request = DescribeDomainRecordsRequest()
    request.set_DomainName(dns_domain)
    request.set_accept_format(rc_format)
    result = clt.do_action(request).decode('utf-8')
    result = json.JSONDecoder().decode(result)
    return result

def addArecord(ipv4):
    client = AcsClient(accessKeyId, accessSecret, 'cn-hangzhou')
    request = AddDomainRecordRequest()
    request.set_accept_format(rc_format)
    request.set_Value(ipv4)
    request.set_Type("A")
    request.set_RR("useless")
    request.set_DomainName(dns_domain)
    response = client.do_action_with_exception(request)
    print(str(response, encoding='utf-8'))  

"""
???????????????????????????????????????
"""
def updateDns(dns_rr, dns_type, dns_value, dns_record_id, dns_ttl, dns_format):
    clt = AcsClient(accessKeyId, accessSecret, 'cn-hangzhou')
    request = UpdateDomainRecordRequest()
    request.set_RR(dns_rr)
    request.set_Type(dns_type)
    request.set_Value(dns_value)
    request.set_RecordId(dns_record_id)
    request.set_TTL(dns_ttl)
    request.set_accept_format(dns_format)
    result = clt.do_action(request)
    return result

"""
????????????????????????ID??????????????????IP??????
"""
def getOldIp(record_id):
    clt = AcsClient(accessKeyId, accessSecret, 'cn-hangzhou')
    request = DescribeDomainRecordInfoRequest()
    request.set_RecordId(record_id)
    request.set_accept_format(rc_format)
    result = clt.do_action(request)
    result = json.JSONDecoder().decode(result.decode('utf-8'))
    result = result['Value']
    return result

def updateAllDns():
    # disconnect VPN before update DDNS
    disconnectVpn()
    dns_records = checkRecords(dns_domain)
    # ?????????????????????IP
    current_ip = get_internet_ip()
    numOfRC = checkRecords(dns_domain)['TotalCount']
    dns_records = checkRecords(dns_domain)['DomainRecords']['Record']
    rc_rr_list = []
    for i in range(numOfRC):
        rc_rr_list.append(dns_records[i]['RR'])
    
    for rc_rr in rc_rr_list:
        ## ?????????????????????
        old_ip = ""
        record_id = ""
        for record in dns_records:
            if record["Type"] == 'A' and record["RR"] == rc_rr:
                record_id = record["RecordId"]
                print("%s.%s recordID is %s" % (record["RR"],dns_domain,record_id))
                logger.info("%s.%s recordID is %s" % (record["RR"],dns_domain,record_id))
                if record_id != "":
                    old_ip = getOldIp(record_id)
                    break
        
        if record_id  == "":
            print(('Warning: Can not find record_id with A record: %s in %s. Please add it first!')%(rc_rr,dns_domain))
            logger.info(('Warning: Can not find record_id with A record: %s in %s. Please add it first!')%(rc_rr,dns_domain))
            continue

        print("%s.%s now host ip is %s, dns ip is %s" % (rc_rr, dns_domain, current_ip, old_ip))
        logger.info("%s.%s now host ip is %s, dns ip is %s" % (rc_rr, dns_domain, current_ip, old_ip))

        if old_ip == current_ip:
            print("The specified value of A record Value is the same as old, canceling the update")
            logger.info("The specified value of A record Value is the same as old, canceling the update")
        else:
            rc_type = 'a'               # ????????????, DDNS??????A??????
            rc_value = current_ip           # ?????????????????????
            rc_record_id = record_id    # ??????ID
            rc_ttl = '600'             # ??????????????????????????????TTL,??????:???
            
            print(updateDns(rc_rr, rc_type, rc_value, rc_record_id, rc_ttl, rc_format))
            logger.info(updateDns(rc_rr, rc_type, rc_value, rc_record_id, rc_ttl, rc_format))
    

if __name__ == '__main__':
    updateAllDns()