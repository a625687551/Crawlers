# -*- coding: utf-8 -*-

'test'

from lxml import etree
from bs4 import BeautifulSoup
import requests
import json
from selenium import webdriver
from requests.auth import AuthBase
from requests.auth import HTTPBasicAuth

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

class Solution:
    # @param {int[]} A an integer array
    # @return nothing
    def sortIntegers(self, A):
        # Write your code here
        for i in range(len(A) - 1):
            for j in range(i + 1, len(A)):
                if A[i] > A[j]:
                    temp = A[i]
                    A[i] = A[j]
                    A[j] = temp
        return A

