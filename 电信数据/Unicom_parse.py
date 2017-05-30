# usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = 'wangjianfeng'

import requests
import re
import time
import http.cookiejar as cookielib
from selenium import webdriver
from bs4 import BeautifulSoup

# 构造request headers
agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'
headers = {
    'User-Agent': agent,
    'Content-Type': 'text/plain;charset=UTF-8',
    'Cache-Control': 'max-age=0',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Connection': 'Keep-Alive',
}

# 使用cookies信息登录
session = requests.session()
session.cookies = cookielib.LWPCookieJar(filename='cookies_unicom')
try:
    session.cookies.load(ignore_discard=True)
except:
    print('cookies未能加载')


class unicom_parse(object):
    def __init__(self, username, password):
        self.username, self.password = str(username), str(password)
        print(self.username, self.password)

    def Call_detail_parse(self):
        post_url = 'http://iservice.10010.com/e3/static/query/callDetail?_=1479795143774&menuid=000100030001'
        post_data = {
            'pageNo': '1', 'pageSize': '20', 'beginDate': '2016-11-01', 'endDate': '2016-11-22'
        }
        # page_source=requests.get(url,cookies=cookies)
        # page_source=requests.post(url,data=cookies)
        # print(page_source.text)

    def Is_login(self):
        url = "http://iservice.10010.com/e3/static/check/checklogin/?_=1479963186816"
        check_page = session.get(url, headers=headers, allow_redirects=False)
        login_code = check_page.status_code
        if login_code == 200:
            return True
        else:
            return False
        print(check_page)

    def User_login(self):
        post_url = "https://uac.10010.com/portal/Service/MallLogin?callback=jQuery17209332841114299033_" \
                   "1420279331097&redirectURL=http%3A%2F%2Fwww.10010.com&userName=" + self.username + "&password=" \
                   + self.password + "&pwdType=01&productType=04&redirectType=01&rememberMe=1&areaCode=841" \
                                     "&arrcity=%E8%A5%BF%E5%AE%89"
        # post_data = {
        #     'userName': '18665961559', 'userPwd': '066530'
        # }
        # login_page=session.post(post_url,data=post_data,headers=headers)
        login_page = session.get(post_url, headers=headers)
        login_code = login_page.text
        print(login_page.status_code, login_code)
        session.cookies.save()
        self.Is_login()  # 检查登陆成功否


if __name__ == '__main__':
    ac = unicom_parse(18665961559, '066530')
    ac.User_login()
    # print(temp)

'https://uac.10010.com/oauth2/new_auth?display=wap&page_type=05&real_ip=106.39.79.162'
'http://iservice.10010.com/e3/static/check/checklogin/?_=1479789247653'
"https://uac.10010.com/portal/Service/MallLogin?callback=?"
'''
CommonConstants.LOGIN_URL = UacPrefix.PRXFIX_HTTPS_URL + "/portal/Service/MallLogin?callback=?";
CommonConstants.LOGIN_UNICOM_URL = UacPrefix.PRXFIX_HTTPS_URL + "/portal/Service/LoginUnicom?callback=?";

UacPrefix.PRXFIX_HTTPS_URL = "https://uac.10010.com"

检查对比4648
url: CommonConstants.LOGIN_URL + "?req_time=" + new Date().getTime()
CommonConstants.LOGIN_URL = "/oauth2/new_auth"
'https://uac.10010.com/oauth2/new_auth'+'?req_time='+

loginCommon.getLoginParas = function() {
    var params = {};
    params.app_code = $.query.get("app_code");
    params.user_id = $("#userName").val().trim();
    params.user_pwd = $("#userPwd").val().trim();
    params.user_type = $("#userType").val();
    params.pwd_type = $("#pwdType").val();
    params.display = "web";
    params.response_type = "code";
    params.redirect_uri = $.query.get("redirect_uri");
    params.is_check = "1";
    if (loginCommon.isShowVerify == "0") {
        params.verify_code = $("#verifyCode").val();
        params.uvc = $("#uvc").val();
    }
    params.state = $.query.get("state");
    return params;
}

'''
