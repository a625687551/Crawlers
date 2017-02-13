# usr/bin/env python3
#-*- conding: utf-8 -*-

' crawl liaoxuefeng python3 tutorial'

__author__='wangjianfeng'

from bs4 import BeautifulSoup
import requests
import os
import re
import time
import logging
import pdfkit

def parse(url):
    '''

    :param url:
    :return:
    '''
    response=requests.get(url)
    return BeautifulSoup(response.content,'html.parser')

def parse_url_to_html(url,name):
    '''
    :param url:
    :param name:
    :return:url
    '''
    soup=parse(url)

    body=soup.find('div',class_='x-wiki-content')
    title=soup.find('h4').get_text()

    print(body)
def get_url_list():
    '''

    :return: url
    '''
    soup=parse(url='http://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000')
    menu_tag=soup.find_all('ul',class_='uk-nav uk-nav-side')[1]

    urls=[]
    for i in menu_tag.find_all('li'):
        url = 'http://www.liaoxuefeng.com'+i.a.get('href')
        #name = i.a.get_text()
        urls.append(url)
    return urls

def save_pdf(htmls,file_name):
    pass

def main():
    urls=get_url_list()
    htmls=[parse_url_to_html(url,str(index)+'.html')for index,url in enumerate(urls)]

if __name__ == '__main__':
    main()
