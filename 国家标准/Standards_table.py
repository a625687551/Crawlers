#usr/bin/env python3
# -*- coding:utf-8 -*-

__author__='fanxing'

import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import json
import time
from sqlalchemy import create_engine
from selenium import webdriver

url = 'http://www.sac.gov.cn/was5/web/search?channelid=97779&templet=gjcxjg_detail.jsp&searchword=STANDARD_CODE=%27GB/T%2033174-2016%27&XZ=T&STANDARD_CODE=GB/T%2033174-2016'
user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
             'Chrome/54.0.2840.99 Safari/537.36'
headers = {'User-Agent': user_agent,
           'Referer': 'http:/www.sac.gov.cn'}
wb_data = requests.get(url, headers=headers)
soup = BeautifulSoup(wb_data.text, 'lxml')

# 抓取内容：
contents = []
for i in soup.select('tr'):
    contents.append(i.get_text('\t', True))

pattern = re.compile(r"(标准号\tStandard No.|中文标准名称\tStandard Title in Chinese|英文标准名称\tStandard Title in English|" \
                     "发布日期\tIssuance Date|实施日期\tExecute Date|首次发布日期\tFirst Issuance Date|标准状态\tStandard State|" \
                     "复审确认日期\tReview Affirmance Date|计划编号\tPlan No.|代替国标号\tReplaced Standard|" \
                     "被代替国标号\tReplaced Standard|废止时间\tRevocatory Date|采用国际标准号\tAdopted International Standard No.|" \
                     "采标名称\tAdopted International Standard Name|采用程度\tApplication Degree|" \
                     "采用国际标准\tAdopted International Standard|国际标准分类号\t\(ICS\)|" \
                     "中国标准分类号\t\(CCS\)|标准类别\tStandard Sort|标准页码\tNumber of Pages|" \
                     "标准价格\(元\)\tPrice\(￥\)|主管部门\tGovernor|" \
                     "归口单位\tTechnical Committees|起草单位\tDrafting Committee)" \
                     "\t?")

result_list = []
result = []
for content in contents:
    # print(re.split(pattern, content))
    result.extend(re.split(pattern, content))
    result_list.extend(re.findall(pattern, content))

# print(result,'\n',result_list)
data = {}
for i in result_list:
    result_index = result.index(i) + 1
    # print(result_index)
    data[i.split('\t')[0]] = result[result_index].strip()
    print(i.split('\t')[0], result[result_index])
