# usr/bin/env python3
# -*- conding: utf-8 -*-

' crawl liaoxuefeng python3 tutorial'

from bs4 import BeautifulSoup
import requests
import os
import re
import time
import logging
import pdfkit

__author__ = 'maomaochong'

html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
</head>
<body>
{content}
</body>
</html>
"""


def parse(url):
    '''
    封装请求过程
    :param url:解析地址
    :return:soup
    '''
    response = requests.get(url)
    return BeautifulSoup(response.content, 'html.parser')


def parse_url_to_html(url, name):
    '''
    解析URL，并且返回HTML
    :param url:解析的URL
    :param name:HTML保存名字
    :return:HTML
    '''
    try:
        # 获取内容和标题
        soup = parse(url)
        body = soup.find('div', class_='x-wiki-content')
        title = soup.find('h4').get_text()
        # 标题添加到正文最前面，并且居中显示
        center_tag = soup.new_tag('center')
        title_tag = soup.new_tag('h1')
        title_tag.string = title
        center_tag.insert(1, title_tag)
        body.insert(1, center_tag)
        html = str(body)
        # body中的img标签的src由相对路径改为绝对路径
        pattern = "(<img .*?src=\")(.*?)(\")"

        def func(m):
            if not m.group(2).startswith('http://'):
                rtn = m.group(1) + 'http://www.liaoxuefeng.com' + m.group(2) + m.group(3)
                # print('m1 是',m.group(1),'m2 是',m.group(2),'m3 是',m.group(3))# 测试代码
                return rtn
            else:
                return m.group(1) + m.group(2) + m.group(3)

        html = re.compile(pattern).sub(func, html)
        html = html_template.format(content=html)
        html = html.encode('utf-8')
        with open(name, 'wb') as f:
            f.write(html)
        print(title, u'网页下载完毕')
        return name
    except Exception as e:
        logging.error(u'解析错误', exc_info=True)


def get_url_list():
    '''
    获取所有URL目录
    :return: urls
    '''
    soup = parse(url='http://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000')
    menu_tag = soup.find_all('ul', class_='uk-nav uk-nav-side')[1]

    urls = []
    for i in menu_tag.find_all('li'):
        url = 'http://www.liaoxuefeng.com' + i.a.get('href')
        name = i.a.get_text()
        print(url, name)
        urls.append(url)
    return urls


def save_pdf(htmls, file_name):
    '''
    所有的HTML文件保存为PDF文件
    :param htmls:HTML文件列表
    :param file_name:PDF文件名字
    :return:
    '''
    options = {
        'page-size': 'Letter',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': "UTF-8",
        'custom-header': [
            ('Accept-Encoding', 'gzip')
        ],
        'cookie': [
            ('cookie-name1', 'cookie-value1'),
            ('cookie-name2', 'cookie-value2'),
        ],
        'outline-depth': 10,
    }
    pdfkit.from_file(htmls, file_name)
    print(u'合成完毕')


def main():
    start = time.time()
    urls = get_url_list()
    file_name = u"廖雪峰Python3教程.pdf"
    htmls = [parse_url_to_html(url, str(index) + '.html') for index, url in enumerate(urls)]
    save_pdf(htmls, file_name)

    for html in htmls:
        os.remove(html)
    total_time = time.time() - start
    print(u'总共耗时{}秒'.format(total_time))


if __name__ == '__main__':
    main()
    # parse_url_to_html(url='http://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000', name='1')
