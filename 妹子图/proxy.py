import requests
import re
import random

iplist = []
html = requests.get('http://haoip.cc/tiqu.htm')
iplistn = re.findall(r'r/>(.*?)<br/>', html.text, re.S)
for i in iplistn:
    i = re.sub('\n', '', i)
    iplist.append(i.strip())
    print(i.strip())
IP = ''.join(str(random.choice(iplist)).strip())
print(IP)
proxy = {'http': IP}
print(proxy)
