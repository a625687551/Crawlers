import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
import re
import os
from urllib.request import urlopen

start_url = 'https://mm.taobao.com/search_tstar_model.htm?'


def main(start_url):
    driver = webdriver.PhantomJS(executable_path='D:\\Program Files\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe')
    driver.get(start_url)
    bsObj = BeautifulSoup(driver.page_source, 'lxml')
    for single in bsObj.select('a.item-link'):
        MMsinfourl = single.get('href')
        imageurl = single.select('div.img img')[0].get('src') if single.find_all('img',
                                                                                 {'src': re.compile('.*?.jpg')}) else \
        single.select('div.img img')[0].get('data-ks-lazyload')
        print(MMsinfourl, imageurl)
        url = 'https:' + imageurl
        html = urlopen(url)
        data = html.read()  # 解析图片中的数据
        fileName = '/D:/学习/GitHub/Spyder/TaobaoMM/photo/mm' + str(number) + '.jpg'
        fph = open(fileName, 'wb')
        print("[+]Loadinging MM........... " + fileName)
        fph.write(data)
        fph.close()
        fph.flush()


def mkdir(path):
    isExists = os.path.exists(path)
    if not isExists:
        print('[*]偷偷的建立一个名字叫' + path + '的文件夹')
        os.makedirs(path)
    else:
        print('[+]名字为' + path + '的文件夹已经创建成功')


def owninfo(MMurl):
    owndriver = webdriver.PhantomJS(executable_path='D:\\Program Files\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe')
    owndriver.get(MMurl)
    ownObj = BeautifulSoup(owndriver.page_source, 'lxml')
    perMMimg = ownObj.select('#J_ScaleImg > img:attr(src)')
    print(perMMimg)


# test

owninfo('https://mm.taobao.com/self/aiShow.htm?spm=719.7763510.1998643336.1.uavQn0&userId=290551947')
