#！usr/bin/env python3
# -*- coding='utf-8' -*-
author='wangjianfeng'

import requests
from bs4 import BeautifulSoup
import time,datetime
import os
from datetime import datetime,timedelta
from pymongo import MongoClient
from Download import request


class meizi():
    def mkdir(self,path):#创建文件夹保存
        path=path.strip()
        isExist=os.path.exists(os.path.join('/home/rising/图片/meizitu',path))
        if not isExist:
            print(u'创建一个名叫：',path,u'的文件夹','时间是',datetime.datetime.now())
            os.mkdir(os.path.join('/home/rising/图片/meizitu',path))
            return True
        else:
            print(u'名叫：',path,u'的文件夹已经存在','时间是',datetime.datetime.now())
            return False
    def all_url(self,start_url):
        start_html = request.get(start_url,3)
        soup = BeautifulSoup(start_html.text, 'lxml')
        li_list = soup.find('div', {'class': 'all'}).find_all('a')
        for li in li_list:
            title = li.get_text()
            print(u'开始保存：',title)
            path=str(title).replace('?','_')
            self.mkdir(path)#调用mkdir函数来创建文件夹
            os.chdir('/home/rising/图片/meizitu/'+path)#切换到对应的目录
            href = li['href']
            self.html(href)
    def html(self,href):
        html = request.get(href,3)
        html_soup = BeautifulSoup(html.text, 'lxml')
        max_span = html_soup.find('div', class_="pagenavi").find_all('span')[-2].get_text()
        for page in range(1, int(max_span) + 1):
            page_url = href + '/' + str(page)
            self.img(page_url)
            time.sleep(3)
    def img(self,page_url):
        img_html = request.get(page_url,3)
        img_soup = BeautifulSoup(img_html.text, 'lxml')
        img_url = img_soup.find('div', class_="main-image").find('img')['src']
        self.save(img_url)
    def save(self,img_url):
        name = img_url[-9:-4]
        print(u'开始保存',img_url)
        img = request.get(img_url,3)
        with open(name + '.jpg', 'ab') as f:
            f.write(img.content)
            # time.sleep(0.5)

# if __name__=='_main_':
Mzitu=meizi()##实例化
Mzitu.all_url('http://www.mzitu.com/all')##给函数all_url传入参数，启动爬虫（入口）