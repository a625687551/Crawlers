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

js1 = '''() =>{
           Object.defineProperties(navigator,{
             webdriver:{
               get: () => false
             }
           })
        }'''

js2 = '''() => {
            alert (
            window.navigator.webdriver
            )
        }'''

js3 = '''() => {
            window.navigator.chrome = {
            runtime: {},
            // etc.
            };
        }'''

js4 = '''() =>{
            Object.defineProperty(navigator, 'languages', {
                get: () => ['en-US', 'en']
            });
        }'''

js5 = '''() =>{
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5,6],
            });
        }'''


async def main(username, pwd, url):
    # browser = await launch()  # 不打开浏览器，无头浏览
    browser = await launch({
        'headless': False,
        'args': [
            '--disable-extensions',
            '--no-sandbox',
        ],
    })
    page = await browser.newPage()
    await page.setUserAgent(
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36')
    await page.goto(url)
    await page.evaluate(js1)
    await page.evaluate(js3)
    await page.evaluate(js4)
    await page.evaluate(js5)
    await page.type('.J_UserName', username, {'delay': input_time_random() - 50})
    time.sleep(2)
    await page.type('#J_StandardPwd input', pwd, {'delay': input_time_random() - 50})
    await page.screenshot({'path': './headless-test-result.png'})  # 截图测试
    time.sleep(2)
    # 检测是否有滑块
    # 滑块代码<div id="nocaptcha" class="nc-container tb-login" data-nc-idx="1" style="display: block;">
    slider = await page.Jeval('#nocaptcha',
                              'node => node.style')
    print('判断滑块====》', slider)
    if slider:
        print('存在滑块')
        await page.screenshot({'path': './headless-login-slide.png'})
        flag, page = await mouse_slide(page=page)
        if flag:
            await page.evaluate('''document.getElementById("J_SubmitStatic").click()''')  # 调用js模拟点击登录按钮。
            print("print Enter", flag, page)
            time.sleep(2)
        else:
            print("print enter:", flag, page)
    else:
        print("不存在滑块")
        await page.evaluate('''document.getElementById("J_SubmitStatic").click()''')

        try:
            global error  # 检测是否是账号密码错误
            error = await page.Jeval('.error', 'node => node.textContent')
            print("error:", error)
        except Exception as e:
            error = None
            print('发生错误：', e)
    time.sleep(2)
    await tianmao(page)
    await page.close()


# 有个检测机制，要模仿人类的输入方式
def input_time_random():
    return random.randint(100, 151)


# 如果返回的结果是None，重新尝试移动滑块
def retry_if_result_none(result):
    return result is None


@retry(retry_on_result=retry_if_result_none, )
async def mouse_slide(page=None):
    await asyncio.sleep(2)
    try:
        print('开始验证。。。')
        await page.hover('#nc_1_n1z')
        await page.mouse.down()
        # 这里测试下(x,y)
        await page.mouse.move(700, 0, {'delay': input_time_random() * 5})
        await page.mouse.up()
    except Exception as e:
        print(e, ':滑块验证失败')
        return None, page
    else:
        await asyncio.sleep(2)
        slider_twice = await page.Jeval('.nc-lang-cnt', 'node => node.textContent')
        if slider_twice != '验证通过':
            return None, page
        else:
            await page.screenshot({'path': './headless-slide-result.png'})  # 截图测试
            print('验证通过')
            return 1, page


async def get_cookie(page):
    cookies_list = await page.cookies()
    cookies = ''
    for cookie in cookies_list:
        str_cookie = '{0}={1};'
        str_cookie = str_cookie.format(cookie.get('name'), cookie.get('value'))
        cookies += str_cookie
    return cookies


async def tianmao(page):
    print('跳转天猫店铺=====》')
    # 渲染JS
    await page.setJavaScriptEnabled(enabled=True)
    await page.goto('https://thermos.tmall.com/search.htm')
    await asyncio.sleep(2)
    # 抓取各个信息列表
    element_list = await page.xpath('//div[@class="J_TItems"]//dd[@class="detail"]')
    for item in element_list:
        good_name = await item.xpath('./a').getProperty('textContent')
        good_link = await item.xpath('./a').getProperty('href')
        good_price = await item.xpath('.//span[@class="c-price"]').getProperty('textContent')
        print(good_name, good_link, good_price)


if __name__ == '__main__':
    """手机验证码真的是无语"""
    username = '2222'  # 账号
    pwd = '22222'  # 密码
    url = 'https://login.taobao.com/member/login.jhtml?style=mini&from=b2b&full_redirect=true'  # 淘宝登录地址
    # loop = asyncio.get_event_loop()  # 事件循环，开启个无限循环的程序流程，把一些函数注册到事件循环上。当满足事件发生的时候，调用相应的协程函数。
    # result = loop.run_until_complete(main(username, pwd, url))  # 将协程注册到事件循环，并启动事件循环
    # print('登录后:', result)
    asyncio.get_event_loop().run_until_complete(main(username, pwd, url))
