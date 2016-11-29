
# coding: utf-8

# In[1]:

import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import json
import time
from sqlalchemy import create_engine
from selenium import webdriver


# In[157]:

class phantomjs_SS(object):
    def __init__(self, url):
        '''
        使用Shadowscoks代理，代理端口1080，可测试网址：www.ip.cn；
        采用动态页面解决方案Selenium+PhantomJS；
        初始化——BeautifulSoup解析网址后的生成内容soup
        '''
        service_args = ['--proxy=localhost:1080', '--proxy-type=socks5', ]
        driver = webdriver.PhantomJS(executable_path="C:\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe",service_args=service_args)
        driver.get(url)
        self.soup = BeautifulSoup(driver.page_source, 'lxml')
        driver.close()
        
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
                y = i.strip().split('：',1)
                data[y[0]] = y[1]

        data_keys = [ '标准号', '标准名称', '英文名称', '标准状态','适用范围',
                     '首发日期', '发布日期', '实施日期', '出版语种',
                     '标准ICS号', '中标分类号',
                     '替代以下标准', '被以下标准替代', '引用标准', '采用标准', '采标名称', '采标程度', 
                     # '页数', '字数', '开本', '版次', '彩页数', '插页数', '有无电子版', '有无彩色图片', '纸质版出版日期',
                     # '有无修改单', '修改单备注', 
                     '标准类型', '标准属性', '标准编号', '起草人', '起草单位', '归口单位', '提出部门', '发布部门']
        df = pd.DataFrame(data, index=[0], columns= data_keys) 
        # 等同于 pd.DataFrame(pd.Series(data, index=data_keys)).T
        # pd.DataFrame.from_dict(adict, orient= 'index') 等同于 pd.DataFrame(pd.Series(data, index=data_keys))
        return df
    
    def spc_list(self):
        '''
        抓取spc.org.cn标准列表信息。
        网址自定义：
        def spc_url(pageIndex, classcode):
            url='http://www.spc.org.cn/gb168/basicsearch?lang=zh_CN&text=&search=&openmore=cn&'
            urlend = 'pageIndex={}&standclass=CN&classcode={}'.format(str(pageIndex), classcode)
            return url + urlend
        其中：pageIndex为页码，classcode为类别
        [spc_url(i, 'A00') for i in range(1,26)]
        返回：一个数据框
        '''
        standard = []
        for x in self.soup.select(' div.search-left > div'):
            data = {}
            #print(x.get_text())
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
        df = pd.DataFrame(standard, columns=['标准编号', '标准名称', '英文名称','发布日期', '实施日期', '读者对象',  '内容简介'])
        return df

    def db_content(self, dfn, Table = 'spc_content', Database = 'tu'):
        '''
        将标准信息内容存储到mysql数据库
        spc.db_content(spc.spc_content())
        engine = create_engine('mysql+mysqlconnector://[user]:[pass]@[host]:[port]/[schema]', echo=False)
        '''
        engine = create_engine("mysql+pymysql://root:ehs-root@localhost:3306/{0}?charset=utf8".format(Database),
                               echo=False)
        dfn.to_sql(Table ,engine,if_exists='append', index=False)   

    def db_list(self, dfn, Table = 'spc_list', Database = 'tu'):
        '''
        将列表内容存储到mysql数据库
        spc.db_list(spc.spc_list())
        '''
        engine = create_engine("mysql+pymysql://root:ehs-root@localhost:3306/{0}?charset=utf8".format(Database),
                               echo=False)
        dfn.to_sql(Table ,engine,if_exists='append', index=False)   


# In[158]:

url = "http://www.spc.org.cn/gb168/online/GB%252017930-2013/?"
spc = phantomjs_SS(url)


# In[159]:

spc.spc_content()


# In[160]:

spc.db_content(spc.spc_content())




#获取当前时间
def getCurrentTime():
    return time.strftime('[%Y-%m-%d %H:%M:%S]',time.localtime(time.time()))
    
#获取当前时间
def getCurrentDate():
    return time.strftime('%Y%m%d',time.localtime(time.time()))




def spc_url(pageIndex, classcode):
    url='http://www.spc.org.cn/gb168/basicsearch?lang=zh_CN&text=&search=&openmore=cn&'
    urlend = 'pageIndex={}&standclass=CN&classcode={}'.format(str(pageIndex), classcode)
    return url + urlend
# start_url = spc_url(0, 'A00')


# In[169]:

def spc_spider_list(urls, num = 1):
    while len(urls) > 0:
        if num >0:
            urls_error = []
            for url in urls:
                print(getCurrentTime(),'正在抓取：',url, end = ' ')
                try:
                    spc = phantomjs_SS(url)
                    spc.db_list(spc.spc_list())
                    time.sleep(3)
                    print('成功！')
                except:
                    print('\n', getCurrentTime(), '\t############ Error:\t', url)
                    urls_error.append(url)
                    continue
            if len(urls_error)>0:
                print(getCurrentTime(),'@@@@未抓取的链接地址@@@@\n',urls_error)
                time.sleep(5)
                num -= 1 
            urls = urls_error
        else:
            break
    print(getCurrentTime(), "结束")


# In[170]:

urls = [spc_url(i, 'A00') for i in range(1,26)]


# In[171]:

spc_spider_list(urls, num = 1)


