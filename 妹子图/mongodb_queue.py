from datetime import datetime,timedelta
from pymongo import MongoClient,errors

class MogoQueue():
    OUTSTANDING=1##初始状态
    PROCESSING=2##正在下载状态
    COMPLETE=3##下载完成状态

    def __init__(self,db,collection,timeout=300):#初始化mongodb连接
        self.client=MongoClient()
        self.Client=self.client[db]
        self.db=self.Client[collection]
        self.timeout=timeout
    def __bool__(self):
        '''
        这个函数，如果下面执行为真则整个类为真
        '''
        record=self.db.find_one({'status':{'$ne':self.COMPLETE}})
        return True if record else False
    def push(self,url,title):
        try:
            self.db.insert({'_id':url,'status':self.OUTSTANDING,'主题':title})
            print(url,u'插入队列成功')
        except errors.DuplicateKeyError as e:
            print(url,u'已经插入队列了')
            pass
    def push_imgurl(self, url, title):
        try:
            self.db.insert({'_id': title, 'status': self.OUTSTANDING, '主题': url})
            print(url, u'图片插入队列成功')
        except errors.DuplicateKeyError as e:
            print(url, u'地址已经存在')
            pass
    def pop(self):
        '''
        这个函数会查询队列中所有状态为outstanding的值，更改状态，并返回_id
        如果没有outstanding的值则调用repair函数重置超时的outstanding
        $set是重置的意思
        '''
        record=self.db.find_and_modify(
            query={'status':self.OUTSTANDING},
            update={'$set':{'status':self.PROCESSING,'timestamp':datetime.now()}}
        )
        if record:
            return record['_id']
        else:
            self.repair()
            raise KeyError
    def pop_title(self,url):
        record=self.db.find_one({'_id':url})
        return record['主题']
    def peek(self):
        '''这个函数是取出状态为OUTSTANDING的文档并返回_id（url）'''
        record=self.db.find_one({'status':self.OUTSTANDING})
        if record:
            return record['_id']
    def complete(self,url):
        '''这个是更新已完成的url完成'''
        self.db.update({'_id':url},{'$set':{'status':self.COMPLETE}})
    def repair(self):
        '''这个函数是充值状态$lt是比较函数'''
        record = self.db.find_and_modify(
            query={'timestamp':{'$lt':datetime.now()-timedelta(seconds=self.timeout)},'status':{'$ne':self.COMPLETE}},
            update={'$set': {'status': self.OUTSTANDING}}
        )
        if record:
            print(u'重置url状态',record['_id'])
    def clear(self):
        '''这个函数只有第一次调用，这个是删除数据库'''
        self.db.drop()