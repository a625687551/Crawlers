#!usr/bin/env python3
# _*_ coding: utf-8 _*_

"""嗅事百科"""

import requests
import time
import numpy as np
from bs4 import BeautifulSoup

__author__ = 'wangjianfeng'


class QiushiSpier(object):
    def __init__(self):
        pass

    def hot_story(self):
        print(u'loading----')
        page_num = 1
        try_times = 0

        while (1):
            url = 'http://www.qiushibaike.com/8hr/page/' + str(page_num)
            time.sleep(np.random.rand() * 10)
            try:
                page_source = requests.get(url)
                plain_text = page_source.text
                # print('0000')
            except(ConnectionError):
                print('e')
                continue

            soup = BeautifulSoup(plain_text, 'lxml')
            list_soup = soup.find('div', {'id': 'content-left'})

            try_times += 1
            if not list_soup and try_times < 200:
                print('list=0')
                continue
            elif not list_soup or len(list_soup) < 1:
                break

            for story_info in list_soup.findAll('div', {'class': 'article block untagged mb15'}):
                story_author = '作者：' + story_info.find('h2').text.strip()
                story_content = '内容：' + story_info.find('div', {'class': 'content'}).text.strip()
                print(story_author, story_content)

                try_times = 0
            page_num += 1
            print('Downloading Information From Page %d' % page_num)


if __name__ == '__main__':
    qs = Qiushi_spier()
    qs.hot_story()
