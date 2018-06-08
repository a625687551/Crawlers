# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
import random
import requests
import time
import json
import hashlib

from scrapy import signals
from fake_useragent import UserAgent

orderno = "YZ2018675882gvIV3Q&returnType"
secret = "6d44d36fcda34bda881edf72d18d17db"


class BossZhipinSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class RandomUserAgentMiddleware(object):
    def __init__(self, crawler):
        super(RandomUserAgentMiddleware, self).__init__()

        self.ua = UserAgent()
        self.ua_type = crawler.settings.get('RANDOM_UA_TYPE', 'random')

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_request(self, request, spider):
        def get_ua():
            '''Gets random UA based on the type setting (random, firefox…)'''
            return getattr(self.ua, self.ua_type)

        request.headers.setdefault('User-Agent', get_ua())


class RandomProxyMiddleware(object):
    def __init__(self, crawler):
        self.proxy = []

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_request(self, request, spider):
        proxy = self.get_random_proxy()
        print("this is request ip:" + proxy)
        request.meta['proxy'] = proxy
        # 设置代理
        # request.headers['Proxy-Authorization'] = self.get_sign()

    def process_response(self, request, response, spider):
        '''对返回的response处理'''
        # 如果返回的response状态不是200，重新生成当前request对象
        info = json.loads(response.body)
        proxy_try = request.meta.get("proxy_try", 1)
        if response.status != 200:
            proxy = self.get_random_proxy()
            print("this is response ip:" + proxy)
            request.meta['proxy'] = proxy
            # request.headers['Proxy-Authorization'] = self.get_sign()
            return request
        if info["msg"] and proxy_try < 3:
            proxy = self.get_random_proxy()
            print("this is response ip:" + proxy)
            request.meta['proxy'] = proxy
            request.dont_filter = True
            request.meta['proxy_try'] = proxy_try + 1
            return request
        return response

    def get_random_proxy(self):
        '''随机从文件中读取proxy'''
        url = "http://api.xdaili.cn/xdaili-api//greatRecharge/getGreatIp?spiderId=6d44d36fcda34bda881edf72d18d17db&orderno=YZ2018675882gvIV3Q&returnType=2&count=5"
        if self.proxy:
            proxy = self.proxy[-1].strip()
            self.proxy.pop()
        else:
            content = requests.get(url).json()
            time.sleep(5)
            self.proxy = ["https://%s:%s" % (x["ip"], x["port"]) for x in content["RESULT"]]
            print(self.proxy)
            proxy = self.proxy[-1].strip()
            self.proxy.pop()
        return proxy

    def get_sign(self):
        timestamp = str(int(time.time()))  # 计算时间戳
        string = "orderno=" + orderno + "," + "secret=" + secret + "," + "timestamp=" + timestamp
        string = string.encode()

        md5_string = hashlib.md5(string).hexdigest()  # 计算sign
        sign = md5_string.upper()  # 转换成大写
        auth = "sign=" + sign + "&" + "orderno=" + orderno + "&" + "timestamp=" + timestamp
        return auth
