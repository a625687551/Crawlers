# usr/bin/env python3
# -*- coding:utf-8 -*-

import requests
import pandas as pd
import re
import json
import time
from sqlalchemy import create_engine
from bs4 import BeautifulSoup
from selenium import webdriver

__author__ = 'wangjianfeng'


class PhantomjsSs(object):
    #
    def __int__(self, url):
        service_args = ['--proxy=localhost:1080', '--proxy-type=socks5', ]
        driver = webdriver.PhantomJS(executable_path="C:\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe",
                                     service_args=service_args)
        driver.get(url)
        self.soup = BeautifulSoup(driver.page_source, 'lxml')
        driver.close()

    def spc_list(self):
        standard = []
        for x in self.soup.select(' div.search-left > div'):
            data = {}
            print(x.text())
            try:
                data['标准编号'] = list(x.stripped_strings)[0].split('\t')[-1]
                data['标准名称'] = list(x.stripped_strings)[1]
                pattern = r'(?:英文名称|发布日期|实施日期|读者对象|内容简介)\xa0:\n.*'
                for i in re.findall(pattern, x.get_text('\n', True)):
                    y = i.split('\xa0:\n')
                    data[y[0]] = y[1]
                standard.append(data)
            except:
                continue
        df = pd.DataFrame(standard, columns=['标准编号', '标准名称', '英文名称', '发布日期', '实施日期', '读者对象', '内容简介'])
        print(df)
        return df

    def spc_content(self):
        '''
        抓取spc.org.cn具体标准信息。
        网址示例：url = "http://www.spc.org.cn/gb168/online/GB%252017930-2013/?"
        返回：一个数据框df, 数据框的列名为data_keys
        '''
        data = {}
        data['适用范围'] = self.soup.select('#content > div.detailedinfo-top > div > div.detailedinfo-text')[0].get_text()
        contents = self.soup.select('ul.detailedinfo-content-collapse')

        pattern = r'(?:标准号：|标准名称：|英文名称：|标准状态：|适用范围：|首发日期：|发布日期：|实施日期：|出版语种：|标准ICS号：|中标分类号：|替代以下标准|被以下标准替代|引用标准|采用标准|采标名称|采标程度|页数：|字数：|开本：|版次：|彩页数：|插页数：|有无电子版：|有无彩色图片：|纸质版出版日期：|有无修改单：|修改单备注：|标准类型：|标准属性：|标准编号：|起草人：|起草单位：|归口单位：|提出部门：|发布部门：).*\n'
        for content in contents:
            x = content.get_text()
            for i in re.findall(pattern, x):
                y = i.strip().split('：', 1)
                data[y[0]] = y[1]

        data_keys = ['标准号', '标准名称', '英文名称', '标准状态', '适用范围',
                     '首发日期', '发布日期', '实施日期', '出版语种',
                     '标准ICS号', '中标分类号',
                     '替代以下标准', '被以下标准替代', '引用标准', '采用标准', '采标名称', '采标程度',
                     # '页数', '字数', '开本', '版次', '彩页数', '插页数', '有无电子版', '有无彩色图片', '纸质版出版日期',
                     # '有无修改单', '修改单备注',
                     '标准类型', '标准属性', '标准编号', '起草人', '起草单位', '归口单位', '提出部门', '发布部门']
        df = pd.DataFrame(data, index=[0], columns=data_keys)
        # 等同于 pd.DataFrame(pd.Series(data, index=data_keys)).T
        # pd.DataFrame.from_dict(adict, orient= 'index') 等同于 pd.DataFrame(pd.Series(data, index=data_keys))
        print(df)
        return df


if __name__ == '__main__':
    url = "http://www.spc.org.cn/gb168/online/GB%252017930-2013/?"
    spc = PhantomjsSs(url)
    spc.spc_content()
