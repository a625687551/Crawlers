# usr/bin/env python3
# -*- coding: utf-8 -*-

"""
自如有家爬虫
"""

__author__ = 'wangjianfeng'

import time
import requests
import pymongo
import smtplib

from email.mime.text import MIMEText
from bs4 import BeautifulSoup

client = pymongo.MongoClient('localhost', 27017)
ziru = client['ziru']
room_info = ziru['room_info']


class ZiRoom(object):

    def __init__(self):
        pass

    def parse_url(self):  # 爬去列表页的所有网址
        urls = []
        page_num = 1
        while page_num < 3:  # 这里设置多少页，用来获取最新刷新的房源
            time.sleep(1)  # 没有暂停的爬虫就是耍流氓
            url = 'http://www.ziroom.com/z/nl/z2-o1.html?qwd=弘善家园&p={}'.format(page_num)  # 指定网页爬去
            print(url)
            page_source = requests.get(url)
            plain_code = page_source.text
            soup = BeautifulSoup(plain_code, 'lxml')
            url_list = soup.find('ul', {'id': 'houseList'})
            if not url_list:
                break
            for i in url_list.select('div.img.pr > a'):
                urls.append('http:' + i.get('href'))
            page_num += 1
        return (urls)

    def parse_datail(self, url):
        info = {}
        inner_info = [i['room_url'] for i in room_info.find()]  # 提取数据库中所有的房源网页地址用来对比是否是新房子

        plain_code = requests.get(url).text  # 解析网页
        soup = BeautifulSoup(plain_code, 'lxml')  # 解析网页
        info['room_url'] = url
        info['room_name'] = soup.select('div.room_name > h2')[0].string.strip()
        info['price'] = soup.select('span.room_price')[0].string.strip()
        # info['area']=[i.text.strip() for i in soup.select('ul.detail_room > li')]#当时这里嫌弃麻烦有点BUG没有再管了
        # for i in soup.select('ul.detail_room > li'):
        #     print(i.text.strip())
        info['room_id'] = soup.select('h3.fb')[0].text.split('：')[-1].strip()  # 获取房子编号

        if info['room_url'] in inner_info:  # 查看房子是不是在数据库中，在了 就是旧房子不在就是新房子
            print(info)
            print('已经有了')
        else:
            print('哇··新房子出现了')
            room_info.insert_one(info)  # 插入数据库，防止重复找出
            return ('have one!' + info['room_url'])  # 返回一个数据，这个我偷懒了

    def send_email(self, info_send):
        msg = MIMEText(info_send, 'html', 'utf-8')
        msg['From'] = u"*****@163.com"
        msg['To'] = u"*****@qq.com"
        msg['Subject'] = '有新的房子出现了'  # 邮件主题
        try:
            smtp = smtplib.SMTP_SSL('smtp.163.com', 465)
            smtp.set_debuglevel(1)
            smtp.ehlo("smtp.163.com")
            smtp.login(u"****@163.com", u"****")  # 邮箱账号，和第三方客户端授权密码（注意不是邮箱密码）这个需要你去邮箱哪里设置这个
            smtp.sendmail(u"*****@163.com", [u"****@qq.com", u"****@qq.com"], msg.as_string())  # 这里是邮件的格式分别是来源，发送到的邮件地址
            print('发送成功')
        except smtplib.SMTPException:  # 发送不成功，则把错误抛出
            print('错误，无法发送邮件')

    def main(self):  # 这个函数我有些偷懒了，这里编的时间不多，可以修改下，进行房子的筛选（比如价格、大小）
        new_data = {ZiRoom.parse_datail(self, i) for i in ZiRoom.parse_url(self)}
        if len(new_data) < 2:
            print(new_data)
            print('还没有新房子啊·····我等啊等')
        else:
            print('新房子来了···邮件启动')
            print(new_data)
            ZiRoom.send_email(self, '新出来了' + str(len(new_data) - 1) + '套房子')


if __name__ == '__main__':
    while True:  # 定时器，这个定时器不太好，是阻塞式的，可以考虑修改下
        ZiRoom().main()
        time.sleep(60 * 30)
