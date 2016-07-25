# -*- coding: utf-8 -*-

'test'

from lxml import etree
import requests

url='http://tieba.baidu.com/p/3522395718?pn=1'
head=
html=requests.get(url).text
selector = etree.HTML(html)
content_field = selector.xpath('//div[@class="l_post j_l_post l_post_bright  "]')
print(content_field)