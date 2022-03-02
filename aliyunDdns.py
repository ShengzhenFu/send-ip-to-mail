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
from getIp import get_internet_ip
from common import Log

logger = Log()
rc_format = 'json'
dns_domain = domainName

"""
获取域名的解析信息
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
更新阿里云域名解析记录信息
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
根据域名解析记录ID查询上一次的IP记录
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
    dns_records = checkRecords(dns_domain)
    # 获取主机当前的IP
    current_ip = get_internet_ip()
    numOfRC = checkRecords(dns_domain)['TotalCount']
    dns_records = checkRecords(dns_domain)['DomainRecords']['Record']
    rc_rr_list = []
    for i in range(numOfRC):
        rc_rr_list.append(dns_records[i]['RR'])
    
    for rc_rr in rc_rr_list:
        ## 之前的解析记录
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
            rc_type = 'a'               # 记录类型, DDNS填写A记录
            rc_value = current_ip           # 新的解析记录值
            rc_record_id = record_id    # 记录ID
            rc_ttl = '600'             # 解析记录有效生存时间TTL,单位:秒
            
            print(updateDns(rc_rr, rc_type, rc_value, rc_record_id, rc_ttl, rc_format))
            logger.info(updateDns(rc_rr, rc_type, rc_value, rc_record_id, rc_ttl, rc_format))


if __name__ == '__main__':
    updateAllDns()