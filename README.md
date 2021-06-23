# A tool to get your home public IP address and send it to your mailbox
## working logic
```
the program will read previous IP from cache-ip.txt then compare it with current public IP,
if the IP is same, then it will not send out email
if the IP changed, it will send out email with the latest public ip

```
## how to run
```
python sendmail.py
```