#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'douban movies top250'

_author_='wangjianfeng'

import requests,time
from bs4 import BeautifulSoup
import pymongo

client=pymongo.MongoClient('localhost',27017)
douban=client['douban']
movie_info=douban['movie_info']


def get_info(url):
    web_data=requests.get(url).text
    soup=BeautifulSoup(web_data,'lxml')
    movies=soup.select('div.item')
    for single_one in movies:
        data={
            'movie_id': single_one.select('div.pic > em')[0].text,
            'movie_name':single_one.select('div.hd > a > span:nth-of-type(1)')[0].text,
            'movie_score': single_one.select('span.rating_num')[0].text,
            'movie_quote': single_one.select('span.inq')[0].text if single_one.find_all('span','inq') else  None,
            'movie_classify':single_one.select('div.bd > p:nth-of-type(1)')[0].text.split('\xa0')[-1].strip(),
        }
        print(data)
        movie_info.insert_one(data)

if __name__=='__main__':
    urls=['https://movie.douban.com/top250?start={}&filter='.format(str(i)) for i in range(0,250,25)]
    for single_url in urls:
        get_info(single_url)
        print(single_url,'let me have a rest------------')
        time.sleep(5)

    print(u'搞定一切')
    #test
    # urls ='https://movie.douban.com/top250?start=225&filter='
    # get_info(urls)