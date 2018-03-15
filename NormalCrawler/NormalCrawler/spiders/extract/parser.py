# -*- coding: utf-8 -*-

import os
import re
import sys

import js2py
import psutil
import requests

sys.setrecursionlimit(50000)
JS_PATTERN = re.compile(r"<script>(.*?fuck.*?)</script>")
to_insert = r"""
import re
import json
import types
from urllib import unquote
from cStringIO import StringIO
from xml.dom.minidom import parseString

import BeautifulSoup
from js2py.pyjs import *
from js2py.base import PyObjectWrapper


# hook PyObjectWrapper.callprop
def callprop(self, prop, *args):
    if not isinstance(prop, basestring):
        prop = prop.to_string().value
    if prop == 'charAt':
        prop = "__getitem__"
        r = self.get(prop)(*args).to_python().value
        if not isinstance(r, unicode):
            r = r.decode("utf-8")
        return Js(r)
    return tmp_callprop(self, prop, *args)


tmp_callprop = PyObjectWrapper.callprop
PyObjectWrapper.callprop = callprop


# mock document object
soup = BeautifulSoup.BeautifulSoup(StringIO(response_body))
comments = soup.findAll(text=lambda text: isinstance(text, BeautifulSoup.Comment))
for comment in comments:
    comment.extract()
for tag in soup.findAll(True):
    tag.attrs = None
xml = soup.prettify()
document = parseString(xml)
var.put(u"document", Js(document))


# mock window object
class Window(object):
    _data = {}

    def get(self, attr):
        return self._data.get(attr)

    def decodeURIComponent(self, *args):
        # from IPython import embed; embed()
        s = unquote(str(args[0])).decode("utf-8", "ignore")
        return Js(s)

window = Window()
var.put(u"window", Js(window))


# mock method of document
KW_CONTENT_PATTERN = re.compile(r'.hs_kw(\d+)_main.*::before \{ content:(".*?") \}')

class MyDict(object):
    def insertRule(self, *args):
        kw, content = KW_CONTENT_PATTERN.findall(args[0])[0]
        content = json.loads(content)
        kw_content[kw] = content


def querySelectorAll(*args):
    return Js([])


def createElement(self, *args):
    e = tmp_createElement("style")
    if str(args[0]) == "style":
        e.sheet = MyDict()
    return e

tmp_createElement = document.createElement
document.querySelectorAll = types.MethodType(querySelectorAll, document, type(document))
document.createElement = types.MethodType(createElement, document, type(document))
"""


def parse_kw(content):
    kw_content = {}
    response_body = content

    try:
        js = JS_PATTERN.findall(content)[0]  # 提取 js 代码
    except:
        return {}
    pycode = js2py.translate_js(js)  # 转成 python 代码

    # 插入代码
    after_code = "set_global_object(var)"
    pycode = pycode.replace(after_code, "%s\n%s" % (after_code, to_insert))

    d = dict(locals(), **globals())
    exec (pycode, d, d)
    show_memory_info()
    return kw_content


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def show_memory_info():
    pid = os.getpid()
    process = psutil.Process(pid)
    print bcolors.OKBLUE + "Process %s, memory: %s" % (pid, process.memory_info().rss) + bcolors.ENDC


if __name__ == '__main__':
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2986.0 Safari/537.36",
    }

    url = "http://club.autohome.com.cn/bbs/thread-c-4080-61996477-1.html"
    r = requests.get(url, headers=headers)
    print parse_kw(r.content)
