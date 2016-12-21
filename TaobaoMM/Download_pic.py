#!usr/bin/env python3

import requests
import time
import pymongo
import os,re,shutil
from bs4 import BeautifulSoup

header = {
    'accept-language': 'zh-CN,zh;q=0.8,en;q=0.6,en-US;q=0.4',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'origin': 'https://mm.taobao.com',
    'referer': 'https://mm.taobao.com/search_tstar_model.htm?spm=719.7763510.1998606017.2.vcQ5Zq',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}
def downpic():
    client=pymongo.MongoClient('localhost',27017)
    TBMM=client['TBMM']
    MM_info=TBMM['MM_info']
    Model_card=TBMM['Model_card']
    t = 1
    for data in MM_info.find().batch_size(30).limit(10):
        name=data['realName']
        #city=data['city']
        userId=data['userId']
        modelcardurl = 'https://mm.taobao.com/self/info/model_info_show.htm?user_id='+str(userId)
        #modelcardurl = 'https://mm.taobao.com/self/model_info.htm?user_id=' + str(data['userId'])
        # path='F:/photo/'+name+'-'+city
        # mkdir(path)#检查并建立相应的文件夹
        # detailurl=data['detailurl']
        # print(detailurl,path,modelcardurl)
        # getimage(detailurl,path)#获取淘女郎详细图片,在公司网络真是太差了··家里亲测可以 或者是batch_size的原因
        print(name,modelcardurl)
        info=getmodelcard(modelcardurl,userId)
        # info['totalFanNum']=data["totalFanNum"]
        # info['totalFavorNum'] = data["totalFavorNum"]
        Model_card.insert_one(info)
        print(t)
        t += 1


#判断路径是否存在
def mkdir(path):
    #判断路径是否存在
    isExist=os.path.exists(path)
    if not isExist:
        print('创建一个名叫'+path+'文件夹')
        #不存在则创建文件夹
        os.makedirs(path)
    else:
        #存在则提示已经创建完毕
        print('已经创建'+path+'文件夹')
#下载图片函数
def getimage(detailurl,MMpath):
    web_data=requests.get(detailurl,headers=header)
    soup=BeautifulSoup(web_data.text,'lxml')
    time.sleep(2)
    # imageurls=soup.select('div.mm-aixiu-content p img')
    imageurls = soup.find_all('img',{'src':re.compile('.*\.jpg')})
    number = 1#图片进行计数和命名
    for perimgurl in imageurls:
        imagepath='https:'+perimgurl.get('src').strip()
        # time.sleep(1)
        try:
            img=requests.get(imagepath,stream=True,headers=header)
            if img.status_code==200:
                filename = MMpath + '/' + str(number) + '.jpg'
                with open(filename,'wb') as f:
                    # f.write(html.content)
                    print("[+]Loading.......her photo as" + filename)
                    print("[+]Loading.......her photo as " + filename)
                    for chunk in img.iter_content(chunk_size=512*1024):
                        if chunk:
                            f.write(chunk)
                    number += 1
                    f.flush()
        except Exception:
            print('[!]address error!')
def getmodelcard(modelcardurl,userId):
    web_data=requests.get(modelcardurl,headers=header)
    soup=BeautifulSoup(web_data.text,'lxml')
    info={}
    content=soup.select('ul.mm-p-info-cell.clearfix li span')[:7]
    info['name'] = content[0].get_text()
    info['birthday'] = content[1].get_text().split()
    info['city'] = content[2].get_text()
    info['job'] = content[3].get_text()
    info['blood_type'] = content[4].get_text()
    info['school_major'] = content[5].get_text().split()
    info['height']=soup.select('.mm-p-height p')[0].get_text()
    info['weight'] = soup.select('.mm-p-weight p')[0].get_text()
    info['BWH'] = soup.select('.mm-p-size p')[0].get_text()
    info['bar'] = soup.select('.mm-p-bar p')[0].get_text()
    info['shose'] = soup.select('.mm-p-shose p')[0].get_text()
    info['exprience']=soup.select('.mm-p-experience-info p')[0].get_text().split()
    tags=soup.select('ul.mm-p-tag li')
    info['tag'] =[tag.get_text() for tag in tags]
    info['userId']=userId
    print(info)
    return info
if __name__=='__main__':
    testurl='https://mm.taobao.com/self/aiShow.htm?userId=2885596272'
    downpic()
    print('finally........')