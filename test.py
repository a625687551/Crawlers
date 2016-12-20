# -*- coding: utf-8 -*-

'test'

from lxml import etree
from bs4 import BeautifulSoup
import requests
import json
from selenium import webdriver
from requests.auth import AuthBase
from requests.auth import HTTPBasicAuth
from time import ctime,sleep
import _thread

# class Crawl(object):
#     def __init__(self,username,password):
#         self.username,self.password=username,password
#         self.post_data={'username':self.username,
#                    'password':self.password,
#                    }
#         self.post_url='http://pythonscraping.com/pages/cookies/welcome.php'
#     def web_post(self):
#         page_source=requests.post(self.post_url,self.post_data)
#         print(page_source.text)
#         print(page_source.cookies.get_dict())
#         print('---------------')
#         login_page=requests.get('http://pythonscraping.com/pages/cookies/profile.php',cookies=page_source.cookies)
#         print(login_page.text)
#
# if __name__=='__main__':
#     Crawl('wangjianfeng','password').web_post()

#session 方法
# class Crawl(object):
#     def __init__(self,username,password):
#         self.username,self.password=username,password
#         self.post_data={'username':self.username,
#                    'password':self.password,
#                    }
#         self.post_url='http://pythonscraping.com/pages/cookies/welcome.php'
#     def web_post(self):
#         s=requests.session()
#         page_source=s.post(self.post_url,data=self.post_data)
#         print(page_source.cookies.get_dict())
#         print('----------')
#         check_page=s.get('http://pythonscraping.com/pages/cookies/profile.php')
#         print(check_page.text)
#
# if __name__=='__main__':
#     Crawl('wangjianfeng','password').web_post()

def loop0():
    print('start loop0 at ',ctime())
    sleep(4)
    print('loop0 done at ',ctime())
def loop1():
    print('start loop1 at ',ctime())
    sleep(2)
    print('loop0 done at ',ctime())
def main():
    print('starting at ',ctime())
    _thread.start_new_thread(loop0(),())
    _thread.start_new_thread(loop1(),())
    # loop0()
    # loop1()
    sleep(6)
    print('all done at ',ctime())
if __name__=='__main__':
    main()