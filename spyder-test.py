import requests
import re
import random
import time
from bs4 import BeautifulSoup

url='http://www.jycinema.cn/frontUIWebapp/appserver/commonItemSkuService/findItemSku'
params={"cinemaId":"446","showtime":"2017-01-17","type":"queryItemSku","memberLevelName":"","memberId":"","channelCode":"J0002","channelId":"3"}
url1='http://www.jycinema.cn/frontUIWebapp/appserver/cinCinemaFilmViewService/findFilm'
params1={"type":"quickTicket","cityName":"北京市","status":"HOT","statusRE":"RELEASE","channelCode":"J0002","channelId":"3"}
headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36',
    'Cookie':'localCityName=%E5%8C%97%E4%BA%AC%E5%B8%82; JSESSIONID=9D2F3113B8AEB319BD2454019D680E80',
    'Referer':'http://www.jycinema.cn/frontUIWebapp/templates/default/schedule.html?cinemaId=475',
    'RA-Sid':'s_1387_r2x9ak474125_297',
    'RA-Ver':'3.0.6',
    'X-Requested-With':'XMLHttpRequest',
    'Origin':'http://www.jycinema.cn',
    'Host':'www.jycinema.cn',
    'Content-Type':'application/x-www-form-urlencoded;charset=UTF-8',
    'Connection':'keep-alive',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'Accept-Encoding':'gzip, deflate',
    'Accept':'application/json, text/javascript, */*; q=0.01'
}
r=requests.post(url,params=params,headers=headers)
r1=requests.post(url1,params=params1)
print(r1.text)
print(r.text)