import time
from datetime import datetime
import os
import threading
import multiprocessing
from mongodb_queue import MogoQueue
from Download import request
from bs4 import BeautifulSoup

SLEEP_TIME=1
def mzitu_crawler(max_threads=10):
    crawl_queue=MogoQueue('meinvxiezhenji','crawl_queue')##这个是获取URL的队列
    img_queue=MogoQueue('meinvxiezhenji','img_queue')
    def pageurl_crawler():
        while True:
            try:
                url=crawl_queue.pop()
                print(url)
            except KeyError:
                print(u'队列没有数据')
                break
            else:
                img_urls=[]
                req=request.get(url,3).text
                title=crawl_queue.pop_title(url)
                path=str(title).replace('?','')
                mkdir(path)
                os.chdir('F:\meizitu\\'+path)
                max_span=BeautifulSoup(req,'lxml').find('div',class_='pagenavi').find_all('span')[-2].get_text()
                for page in range(1,int(max_span)+1):
                    page_url=url+'/'+str(page)
                    img_url=BeautifulSoup(request.get(page_url,3).text,'lxml').find('div',class_='main-image').find('img')['src']
                    img_urls.append(img_url)
                    save(img_url)##???
                crawl_queue.complete(url)##设置为完成状态
                img_queue.push_imgurl(title,img_urls)
                print(u'插入数据库成功')
    def save(img_url):
        name=img_url[-9:-4]
        print(u'开始保存：',img_url,u'时间为',datetime.now())
        img=request.get(img_url,3)
        with open(name+'.jpg','ab') as f:
            f.write(img.content)

    def mkdir(path):
        path=path.strip()##发现一个错误[Errno 2] No such file or directory: '1/151.jpg'
        isExists=os.path.exists(os.path.join('F:\meizitu', path))
        if not isExists:
            print(u'建了一个名字叫',path,u'的文件夹')
            os.makedirs(os.path.join('F:\meizitu',path))
            return True
        else:
            print(u'名字叫',path,u'的文件夹已经存在了')
            return False

    threads=[]
    while threads or crawl_queue:
        '''
        这里用上craw_queue，也就是__bool__函数的作用，为真则代表我们MongoDB队列里面还有数据threads 或者
        craw_queue为真都代表我们还没有下载完毕，程序会继续执行
        '''
        for thread in threads:
            if not thread.is_alive():##判断是否为空
                threads.remove(thread)
        while len(threads) < max_threads or crawl_queue.peek():#线程池中线程少于max_threads or crawl_queue时候
            thread=threading.Thread(target=pageurl_crawler)##创建线程
            thread.setDaemon(True)##设置守护线程
            thread.start()#启动线程
            threads.append(thread)##添加进入线程队列
        time.sleep(SLEEP_TIME)
def process_crawler():
    process=[]
    num_cpus=multiprocessing.cpu_count()
    print(u'将会启动进程数为',num_cpus)
    for i in range(num_cpus):
        p=multiprocessing.Process(target=mzitu_crawler)#创建进程进行
        p.start()##启动进程
        process.append(p)##添加进入进程队列
    for p in process:
        p.join()##等待进程队里里面的进程结束
if __name__ == '__main__':
    process_crawler()
