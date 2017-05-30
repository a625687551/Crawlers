#!/usr/bin/env python3
# coding=utf-8
# __author__='__tree__'
from bs4 import BeautifulSoup
from urllib.request import urlopen
from selenium import webdriver
import os
import threading
import re, time


def main():
    driver = webdriver.PhantomJS(
        executable_path='D:\\Program Files\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe')  # 浏览器的地址
    driver.get("https://mm.taobao.com/search_tstar_model.htm?")  # 目标网页地址
    bsObj = BeautifulSoup(driver.page_source, "lxml")  # 解析html语言
    fp = open('mm.txt', 'r+', encoding='utf-8')  # 用来将主页上的个人信息存储
    fp.write(driver.find_element_by_id('J_GirlsList').text)  # 获得主页上的姓名、所在城市、身高、体重等信息
    print("[*]OK GET MM's BOOK")
    MMsinfoUrl = bsObj.findAll("a", {"href": re.compile("\/\/.*\.htm\?(userId=)\d*")})  # 解析出MM的个人主页
    imagesUrl = bsObj.findAll("img", {"data-ks-lazyload": re.compile(".*\.jpg")})  # 解析出MM的封面图片
    # print(MMsinfoUrl)
    time.sleep(2)
    items = fp.readlines()
    content1 = []
    n = 0
    m = 1
    while (n < 14):  # 将MM的信息都集合在同一个容器中，方便查询操作
        content1.append([items[n].strip('\n'), items[m].strip('\n')])
        n += 3
        m += 3
    # print (content1)
    content2 = []
    for MMinfoUrl in MMsinfoUrl:
        content2.append(MMinfoUrl["href"])
    # print(content2)
    contents = [[a, b] for a, b in zip(content1, content2)]
    # print(contents)
    i = 0
    while (i < 5):
        print("[*]MM's name:" + contents[i][0][0] + " with " + contents[i][0][1])
        print("[*]saving......" + contents[i][0][0] + "in the folder")
        perMMpageUrl = "http:" + contents[i][1]
        # perMMpageUrl = getperMMpage(perMMpageUrl,)
        path = '/home/shiyanlou/photo/' + contents[i][0][0]
        mkdir(path)  # 建立相应文件夹
        getperMMpageImg(perMMpageUrl, path)
        i += 1
    fp.flush()
    fp.close()
    number = 1
    for imageUrl in imagesUrl:  # 将封面图片存入对应文件夹中
        url = "https:" + str(imageUrl["data-ks-lazyload"])
        html = urlopen(url)
        data = html.read()
        fileName = '/home/shiyanlou/photo/mm' + str(number) + '.jpg'
        fph = open(fileName, "wb")
        print("[+]Loadinging MM........... " + fileName)
        fph.write(data)
        fph.flush()
        fph.close()
        number += 1

    driver.close()


def mkdir(path):
    # 判断路径是否存在
    isExists = os.path.exists(path)
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        print("[*]偷偷新建了名字叫做" + path + "的文件夹")
        # 创建目录操作函数
        os.makedirs(path)
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print("[+]名为" + path + '的文件夹已经创建成功')


def getperMMpageImg(MMURL, MMpath):
    owndriver = webdriver.PhantomJS(executable_path='D:\\Program Files\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe')
    owndriver.get(MMURL)
    time.sleep(2)
    print("[*]Opening.....MM....................")
    ownObj = BeautifulSoup(owndriver.page_source, "lxml")
    perMMimgs = ownObj.findAll("img", {"src": re.compile(".*\.jpg")})  # 获得模特个人页面上的艺术照地址
    number = 2  # 图片计数器
    for perMMimg in perMMimgs:
        ImgPath = "https:" + str(perMMimg["src"])  # 处理成标准的超文本访问信息
        # print(ImgPath)
        try:
            html = urlopen(ImgPath)
            data = html.read()
            fileName = MMpath + "/" + str(number) + '.jpg'
            fp = open(fileName, 'wb')
            print("[+]Loading.......her photo as" + fileName)
            fp.write(data)
            fp.close()
            fp.flush()
            number += 1
        except Exception:
            print("[!]Address Error!!!!!!!!!!!!!!!!!!!!!1")


if __name__ == '__main__':
    main()
