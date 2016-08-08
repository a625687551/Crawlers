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
    movie_name=soup.select('div.hd > a > span:nth-of-type(1)')
    # content > div > div.article > ol > li:nth-child(1) > div > div.info > div.hd > a >
    movie_id=soup.select('div.pic > em')
    # content > div > div.article > ol > li:nth-child(14) > div > div.pic > em
    movie_score=soup.select('span.rating_num')
    movie_quote = soup.select('span.inq')
    movie_classify=soup.select('div.info > div.bd > p:nth-of-type(1)')
    # content > div > div.article > ol > li:nth-child(1) > div > div.info > div.bd > p
    # print(movie_classify)
    for movie_id,movie_name,movie_score,movie_quote,movie_classify in zip(movie_id,movie_name,movie_score,movie_quote,movie_classify):
        data={
            'movie_id': movie_id.get_text(),
            'movie_name':movie_name.get_text(),
            'movie_score': movie_score.get_text(),
            'movie_quote': movie_quote.get_text()if soup.find_all('span','inq') else  None,
            'movie_classify':list(movie_classify.stripped_strings)[1].split('\xa0')[-1],
        }
        print(data)
        # movie_info.insert_one(data)

if __name__=='__main__':
    # urls=['https://movie.douban.com/top250?start={}&filter='.format(str(i)) for i in range(0,250,25)]
    # for single_url in urls:
    #     get_info(single_url)
    #     print(single_url,'let me have a rest------------')
    #     time.sleep(5)

    print(u'搞定一切')
    urls ='https://movie.douban.com/top250?start=225&filter='
    get_info(urls)