# -*- coding: utf-8 -*-

"""
# 代码参考https://www.jianshu.com/p/609c39702814，https://blog.csdn.net/Chen_chong__/article/details/82950968
# js部分直接参照参考
"""

import asyncio
import random
import time
import lxml

from pyppeteer import launch
from retrying import retry

from eva_js import js1, js2, js3, js4, js5


def input_time_random():
    """有个检测机制，要模仿人类的输入方式,估计是一个正太分布验证"""
    return random.randint(100, 151)


async def main(username, pwd, url):
    browser = await launch(
        headless=False
    )
    page = await browser.newPage()
    await page.setUserAgent(
        'Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/72.0.3626.109 Mobile Safari/537.36'
    )
    await page.setViewport(viewport={"width": 411, "height": 731})
    await page.setJavaScriptEnabled(enabled=True)
    await page.goto(url)
    await page.evaluate(js1)
    await page.evaluate(js3)
    await page.evaluate(js4)
    await page.evaluate(js5)
    await page.type('#username', username, {'delay': input_time_random() - 50})
    time.sleep(2)
    await page.type('#password', pwd, {'delay': input_time_random() - 50})
    await page.click("#submit-btn")
    await page.screenshot({'path': './headless-test-result.png'})  # 截图测试
    time.sleep(5)
    # await tianmao(page)
    await page.close()


if __name__ == '__main__':
    username = '13552760745'  # 账号
    pwd = 'python2019'  # 密码
    url = 'https://login.m.taobao.com/login.htm?loginFrom=wap_b2b'  # 淘宝登录地址
    # loop = asyncio.get_event_loop()  # 事件循环，开启个无限循环的程序流程，把一些函数注册到事件循环上。当满足事件发生的时候，调用相应的协程函数。
    # result = loop.run_until_complete(main(username, pwd, url))  # 将协程注册到事件循环，并启动事件循环
    # print('登录后:', result)
    asyncio.get_event_loop().run_until_complete(main(username, pwd, url))
