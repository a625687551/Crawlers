#！usr/bin/env python3
# -*- coding='utf-8' -*-
author='wangjianfeng'

import requests
from bs4 import BeautifulSoup
import time
import os

class meizi(object):
    def request(sefl,url):
        headers={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
        content=requests.get(url,headers=headers)
        return content
    def mkdir(self,path):
        path=path.strip()
        isExist=os.path.exists(os.path.join('/home/rising/图片/meizitu',path))
        if not isExist:
            print(u'创建一个名叫：',path,u'的文件夹','时间是',time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()))
            os.mkdir(os.path.join('/home/rising/图片/meizitu',path))
            return True
        else:
            print(u'名叫：',path,u'的文件夹已经存在','时间是',time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()))
            return False
    def all_url(self,start_url):
        start_html = self.request(start_url)
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
        html = self.request(href)
        html_soup = BeautifulSoup(html.text, 'lxml')
        max_span = html_soup.find('div', class_="pagenavi").find_all('span')[-2].get_text()
        for page in range(1, int(max_span) + 1):
            page_url = href + '/' + str(page)
            self.img(page_url)
            time.sleep(3)
    def img(self,page_url):
        img_html = self.request(page_url)
        img_soup = BeautifulSoup(img_html.text, 'lxml')
        img_url = img_soup.find('div', class_="main-image").find('img')['src']
        self.save(img_url)
    def save(self,img_url):
        name = img_url[-9:-4]
        img = self.request(img_url)
        with open(name + '.jpg', 'ab') as f:
            f.write(img.content)
            # time.sleep(0.5)

# if __name__=='_main_':
Mzitu=meizi()
Mzitu.all_url('http://www.mzitu.com/all')