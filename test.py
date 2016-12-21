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
import datetime
import threading
import re
from atexit import register
from urllib.request import urlopen as uopen

head={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'}
REGEX=re.compile('#([\d,]+)in Books')
amzn='https://www.amazon.com/dp/'
ISBNs={
    '0132269937': 'Core Python Programming',
    '0132356139': 'Python Web Development with Django',
    '0137143419': 'Python Fundamentals',
}
def getranking(isbn):
    # page=requests.get('{}{}'.format(amzn,isbn),headers=head)
    # soup=BeautifulSoup(page.text,'html.parser')
    # print(REGEX.findall(soup.decode('utf-8')))
    page = uopen('{}{}'.format(amzn, isbn))
    soup=page.read()
    page.close()
    print(REGEX.findall(soup))
def showranking(isbn):
    print('{} ranked {}'.format(ISBNs[isbn],getranking(isbn)))
def main():
    print('at',datetime.datetime.now())
    for isbn in ISBNs:
        # showranking(isbn)
        getranking(isbn)

@register
def _atexit():
    print('all done at',datetime.datetime.now())
if __name__ == '__main__':
    main()