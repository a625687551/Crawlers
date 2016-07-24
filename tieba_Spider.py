#!usr/bin/env python3
# -*- coding: utf-8 -*-

'jikexueyuan_course'

_author_='wangjianfeng'

from lxml import etree
from multiprocessing.dummy import Pool as ThreadPool
import requests
import json


def towrite(contentdict):
   f.writelines(u'回帖时间;'+str()+'\n')
   f.writelines(u'回帖内容;' + str() + '\n')
   f.writelines(u'回帖人;' + str() + '\n\n')

def spider(url):
    # html=requests.get(url)
    # selector=etree.HTML(html)
    selector=etree.HTML(requests.get(url))

if __name__=='__main__':
    pool=ThreadPool(4)
    with open('content.txt','a') as f:
        page=[]
        for i in range(1,21):
            newpage='http://tieba.baidu.com/p/3522395718?pn='+str(i)
            page.append(newpage)
        result=pool.map(spider,page)
        pool.close()
        pool.join()
