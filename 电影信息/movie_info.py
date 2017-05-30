import requests
import re
import random
import time
import json
from urllib.parse import quote
from bs4 import BeautifulSoup

headers = {'Accept': 'application/json, text/javascript, */*; q=0.01',
           'Accept-Encoding': 'gzip, deflate',
           'Accept-Language': 'zh-CN,zh;q=0.8',
           'Connection': 'keep-alive',
           'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
           'Host': 'www.jycinema.cn',
           'Origin': 'http//www.jycinema.cn',
           'Referer': 'http//www.jycinema.cn/frontUIWebapp/templates/default/schedule.html?cinemaId=475',
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
           'X-Requested-With': 'XMLHttpRequest'}

cityName = '成都'

url_time = 'http://www.jycinema.cn/frontUIWebapp/appserver/commonItemSkuService/getTime'
data_time = 'params=' + quote(
    json.dumps({"type": "getTime", "cityName": cityName, "channelCode": "J0002", "channelId": "3"},
               ensure_ascii=False).replace(' ', ''))

url_cinema = 'http://www.jycinema.cn/frontUIWebapp/appserver/cinCinemaMessageService/findCinema'
data_cinema = 'params=' + quote(
    json.dumps({"type": "totalCinema", "cityName": cityName, "channelCode": "J0002", "channelId": "3"},
               ensure_ascii=False).replace(' ', ''))

url_data = 'http://www.jycinema.cn/frontUIWebapp/appserver/commonItemSkuService/findItemSku'
# cinemaId = str(cityid)#---->成都的id
data_data = 'params=' + quote(json.dumps(
    {"cinemaId": '446', "showtime": "2017-01-18", "type": "queryItemSku", "memberLevelName": "", "memberId": "",
     "channelCode": "J0002", "channelId": "3"}, ensure_ascii=False).replace(' ', ''))

url_cityid = 'http://www.jycinema.cn/frontUIWebapp/appserver/cinCinemaMessageService/findCinemaByCityName'

session = requests.session()
resp = session.post(url_data, headers=headers, params=bytes(data_data, 'utf-8'), timeout=None)
get_data = json.loads(resp.text)
print(get_data)
