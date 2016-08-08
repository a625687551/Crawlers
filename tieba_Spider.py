#!usr/bin/env python3
# -*- coding: utf-8 -*-

'jikexueyuan_course'

_author_='wangjianfeng'

from lxml import etree
from multiprocessing.dummy import Pool as ThreadPool
import requests
import json



def towrite(contentdict):
   f.writelines(u'回帖人:'+contentdict['usr-name']+'\n')
   f.writelines(u'回帖人-ID:' + str(contentdict['usr-id']) + '\n')
   f.writelines(u'回帖人-SEX:' + str(contentdict['sex']) + '\n')
   f.writelines(u'回帖时间:' + str(contentdict['topic_reply_time']) + '\n')
   f.writelines(u'回帖内容:' + contentdict['topic_reply_content']+ '\n\n')

def spider(url):
    head={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'}
    # html=requests.get(url)
    # selector=etree.HTML(html)
    selector=etree.HTML(requests.get(url,headers=head).text)
    content_field=selector.xpath('//div[@class="l_post j_l_post l_post_bright  "]')
    items={}
    for each in content_field:
        reply_info=json.loads(each.xpath('@data-field')[0].replace('&quot',''))
        items['usr-name']=reply_info["author"]["user_name"]
        items['usr-id']=reply_info["author"]["user_id"]
        items['sex']=reply_info["author"]["user_sex"]
        items['topic_reply_time'] = reply_info['content']['date']
        items['topic_reply_content'] = each.xpath('div[@class="d_post_content_main"]/div/cc/div[@class="d_post_content j_d_post_content  clearfix"]/text()')[0]
        towrite(items)


if __name__=='__main__':
    pool=ThreadPool(4)
    with open('content.txt','a',encoding='utf-8') as f:
        page=[]
        for i in range(1,3):
            newpage='http://tieba.baidu.com/p/3522395718?pn='+str(i)
            page.append(newpage)
        result=pool.map(spider,page)
        pool.close()
        pool.join()
    print('finally....')