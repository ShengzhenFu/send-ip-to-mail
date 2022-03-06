# A tool to send your public IP to your mailbox, and update the IP to Aliyun DDns 
## working logic
```
the program will read previous IP from cache-ip.txt then compare it with your current public IP,
if the IP is same, then it will not send out email
if the IP changed, it will send out email with the latest public ip, and update Aliyun DNS records

### .env file
```
```
OUTLOOK_USER=sender_mail@outlook.com
```
```
OUTLOOK_PWD=your_password
```
```
RECEIVERS=receiver_mail_box
```
```
SENDER=sender_mail@outlook.com
```
```
QQSENDER=sender_mail@qq.com
```
```
QQMAIL_USER=QQ_mail@qq.com
```
```
QQMAIL_PWD=qq_mail_password
```
```
QQMAIL_POP_SMTP_PWD=secret_pop_qq_mail
```
```
QQMAIL_IMAP_SMTP_PWD=secret_imap_qq_mail
```
```
QQMAIL_EXCHANGE_PWD=secret_exchange_qq_mail
```
```
ACCESSKEYID=aliyun_accessKeyId
```
```
ACCESSSECRET=aliyun_accessSecret
```
```
## how to send internet ip to mail 
```
python3 sendmail.py
```
## how to update A record to Aliyun DNS with latest internet ip

```
python3 aliyunDdns.py
```
## if you want to do both 
```
python3 main.py 
```

