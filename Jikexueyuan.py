#!usr/bin/env python3
# -*- coding: utf-8 -*-

'jikexueyuan_course'

_author_='wangjianfeng'

import re
import requests


class Spyder(object):
    def __init__(self):
        print('开始抓取课程信息：\n')
    #获取网页源代码
    def getsource(self,url):
        html=requests.get(url).text
        return html
    #翻页
    def changpage(self,url,total_page=1):
        now_page=int(re.search('pageNum=(\d+)',url,re.S).group(1))
        page_group=[]
        for i in range(now_page,total_page):
            link=re.sub('pageNum=\d+','pageNum=%d'%i,url,re.S)
            page_group.append(link)
        return page_group
    #抓取每个课程信息的内容
    def geteveryclass(self,source):
        everyclass=re.findall('(<li id=.*?</li>)',source,re.S)
        return everyclass
    #从everyclass提取所需要的信息
    def getinfo(self,eachclass):
        info={}
        info['title']=re.search('"lessonimg" title="(.*?)" alt=',eachclass,re.S).group(1)
        info['content']=re.search('<p style="height: 0px; opacity: 0; display: none;">(.*?)</p>',eachclass,re.S).group(1)
        timeandlevel=re.findall('<em>(.*?)</em>',eachclass,re.S)
        info['time']=timeandlevel[0]
        info['level']=timeandlevel[1]
        info['learn-number']=re.search('<em class="learn-number" style="display: none;">(.*?)</em>',eachclass,re.S).group(1)
        return info
    #保存数据
    def saveinfo(self,classinfo):
        with open('info.txt','a') as f:
            for each in classinfo:
                f.writelines('title:'+each['title']+'\n')
                f.writelines('content:'+each['content']+'\n')
                f.writelines('time:'+each['time']+'\n')
                f.writelines('level:'+each['level']+'\n\n')
                f.writelines('learn-number:'+each['level'+'\n\n'])


if __name__=='__main__':
    classinfo=[]
    url='http://www.jikexueyuan.com/course/?pageNum=1'
    jikespyder=Spyder()
    all_links=jikespyder.changpage(url,3)
    for link in all_links:
        print('正在处理页面：'+link)
        html=jikespyder.getsource(link)
        everyclass=jikespyder.geteveryclass(html)
        for each in everyclass:
            info=jikespyder.getinfo(each)
            classinfo.append(info)
    jikespyder.saveinfo(classinfo)