import time
import os
import threading
import multiprocessing
from mongodb_queue import MogoQueue
from Download import request
from bs4 import BeautifulSoup

SLEEP_TIME=1
def mzitu_crawler(max_threads=10):
    crawl_queque=MogoQueue('meinvxiezhenji','crawl_queue')##这个是获取URL的队列
    def pageurl_crawler():
        while True:
            try:
                url=crawl_queque.pop()
                print(url)
            except KeyError:
                print(u'队列没有数据')
                break
            else:
                img_urls=[]
                req=request.get(url,3).text
                title=crawl_queque.pop_title(url)
                mkdir(title)
                os.chdir('D:/meizitu/'+title)
                max_span=BeautifulSoup(req,'lxml').find('div',class_='pagenavi').find_all('span')[-2].get_text()
                for page in range(1,int(max_span)+1):
                    page_url=url+'/'+str(page)
                    img_url=BeautifulSoup(request.get(page_url,3).text,'lxml').find('div',class_='main-'
                                                                                                 'image').find('img')['src']
                    img_urls.append(img_url)
                    save(img_url)##???
                crawl_queque.complete(url)##设置为完成状态
    def save(img_url):
        name=img_url[-9:-4]
        print(u'开始保存：',img_url)
        img=request.get(img_url,3)
        with open(name+'.jpg','ab') as f:
            f.write(img.content)

    def mkdir(path):
        path=path.strip()
        isExists=os.path.exists(os.path.join('D:/meizitu',path))
        if not isExists:
            print(u'建了一个名字叫',path,u'的文件夹')
            os.mkdir(os.path.join('D:/meizitu',path))
            return True
        else:
            print(u'名字叫',path,u'的文件夹已经存在了')
            return False
def process_crawler():
    pass
if __name__ == '__main__':
    process_crawler()