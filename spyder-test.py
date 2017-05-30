import requests
import re
import random
import time
import json
from urllib.parse import quote
from bs4 import BeautifulSoup

session = requests.session()
url = 'http://www.23us.com/class/1'
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Referer': 'http://www.23us.com/'
}

proxy = {'http://58.127.195.141': '80'}
r = requests.get(url=url, headers=headers, proxies=proxy)
soup = BeautifulSoup(r.text.encode('ISO-8859-1'), 'lxml')
# print(r.status_code,r.text.encode('ISO-8859-1'),r.encoding)
print(soup)
