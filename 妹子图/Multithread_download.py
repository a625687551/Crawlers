import time
from datetime import datetime
import os
import re
import string
import threading
import multiprocessing
from mongodb_queue import MogoQueue
from Download import request
from bs4 import BeautifulSoup

SLEEP_TIME=1
def mzitu_crawler(max_threads=10):
    crawl_queue=MogoQueue('meizitu','crawl_queue')##这个是获取URL的队列
    img_queue=MogoQueue('meizitu','img_queue')
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
                os.chdir('F:\meizitu\\'+path)##win
                # os.chdir('/home/rising/图片/meizitu/' + path)  # 切换到对应的目录，乌班图系统
                max_span=BeautifulSoup(req,'lxml').find('div',class_='pagenavi').find_all('span')[-2].get_text()
                for page in range(1,int(max_span)+1):
                    page_url=url+'/'+str(page)
                    img_url=BeautifulSoup(request.get(page_url,3).text,'lxml').find('div',class_='main-image').find('img')['src']
                    img_urls.append(img_url)
                    save(img_url)
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
        path=re.sub(r'\\/:*?"<>|','',path.strip())##避免出现照片名字出现各种符号无法命名
        # path=''.join([i for i in path if i not in string.punctuation])##另一个方法
        isExists=os.path.exists(os.path.join('F:\meizitu', path))
        # isExists = os.path.exists(os.path.join('/home/rising/图片/meizitu', path))#Ubuntu
        if not isExists:
            print(u'建了一个名字叫',path,u'的文件夹')
            os.makedirs(os.path.join('F:\meizitu',path))
            # os.makedirs(os.path.join('/home/rising/图片/meizitu', path))
            return True
        else:
            print(u'名字叫',path,u'的文件夹已经存在了')
            return False

    threads = []
    while threads or crawl_queue:
        '''
        这里用上crawl_queue，也就是__bool__函数的作用，为真则代表我们MongoDB队列里面还有数据threads 或者
        craw_queue为真都代表我们还没有下载完毕，程序会继续执行
        '''
        print('12')
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

    # pool=multiprocessing.Pool()
    # for i in range(num_cpus):
    #     process.append(pool.apply_async(mzitu_crawler))
    # pool.close()
    # pool.join()

    print('subprocess all done',datetime.now())
if __name__ == '__main__':
    process_crawler()