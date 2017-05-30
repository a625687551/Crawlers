#!/usr/bin/env python3
# -*- coding:utf-8 -*-


import time
import requests
import pymongo
import json


# 发送请求，得到JSON数据，并加工为python字典形式返回
def getnfo(pagenum):
    # time.sleep(1)
    header = {
        'accept-language': 'zh-CN,zh;q=0.8,en;q=0.6,en-US;q=0.4',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://mm.taobao.com',
        'referer': 'https://mm.taobao.com/search_tstar_model.htm?spm=719.7763510.1998606017.2.vcQ5Zq',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    tao_data = {'viewFlag': 'A', 'pageSize': 100, 'currentPage': pagenum}
    try:
        r = requests.post('https://mm.taobao.com/tstar/search/tstar_model.do?_input_charset=utf-8', data=tao_data,
                          headers=header)
    except:
        print('beiju')
        return None
    raw_datas = json.loads(r.text)
    datas = raw_datas['data']['searchDOList']
    print('完成第', pagenum, '页')
    # print(datas)
    # print(datas[0]['userId'])
    return datas


def main():
    client = pymongo.MongoClient('localhost', 27017)
    TBMM = client['TBMM']
    MM_info = TBMM['MM_info']

    for pagenum in range(1, 411):
        # print(pagenum)
        datas = getinfo(pagenum)
        # if datas:
        #     MM_info.insert_many(datas)
        for single in datas:
            single['detailurl'] = 'https://mm.taobao.com/self/aiShow.htm?userId=' + str(single['userId'])
            MM_info.insert_one(single)


if __name__ == "__main__":
    # Getinfo(1)
    main()
