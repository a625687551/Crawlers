# -*- coding: utf-8 -*-

'test'

from lxml import etree
import requests
import json

url='http://tieba.baidu.com/p/3522395718?pn=1'
head={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'}
# html=requests.get(url,headers=head).text
selector = etree.HTML(requests.get(url,headers=head).text)
# content_field = selector.xpath('//div[@class="l_post j_l_post l_post_bright  "]')
content_field = selector.xpath('//div[@class="l_post j_l_post l_post_bright  "]')
# print(content_field)
for each in content_field:
    reply_info=json.loads(each.xpath('@data-field')[0].replace('&quot',''))
    author=reply_info["author"]["user_name"]
    topic_reply_time = reply_info['content']['date']
    content=each.xpath('div[@class="d_post_content_main"]/div/cc/div[@class="d_post_content j_d_post_content  clearfix"]/text()')[0]
    print(author,topic_reply_time,content)
    print('finally.....')