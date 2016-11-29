import re
import requests
import os
import time
import http.cookiejar as cookielib
from bs4 import BeautifulSoup
from PIL import Image

#构造requests headers
agent='Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.23 Mobile Safari/537.36'
headers = {
    "Host": "www.zhihu.com",
    "Referer": "https://www.zhihu.com/",
    'User-Agent': agent
}
#使用cookies信息登录
session=requests.session()
session.cookies=cookielib.LWPCookieJar(filename='cookies')
try:
    session.cookies.load(ignore_discard=True)
except:
    print('cookies 未能加载')

def get_xsrf():
    '''xsrf是一个动态参数'''
    index_url='https://www.zhihu.com/'
    #获取登录时候用到的xsrf
    index_page=session.get(index_url,headers=headers)
    html=index_page.text
    pattern=r'name="_xsrf" value="(.*?)"/>'
    #这里的_xsrf返回的是一个list
    _xsrf=re.findall(pattern,html)
    print(_xsrf)
    return _xsrf[0]
#获取验证码
def get_captcha():
    t=str(int(time.time()*1000))
    captcha_url= 'http://www.zhihu.com/captcha.gif?r=' + t + "&type=login"
    r=session.get(captcha_url,headers=headers)
    with open('captcha.jpg','wb') as f:
        f.write(r.content)
        # f.close()
    # 用pillow 的 Image 显示验证码
    # 如果没有安装 pillow 到源代码所在的目录去找到验证码然后手动输入
    try:
        im=Image.open('captcha.jpg')
        im.show()
        im.close()
    except:
        print(u'请到%s目录找到captcha.jpg手动输入'%os.path.abspath('captcha.jpg'))
    captcha=input('please input captcha \n')
    print('captcha code'+captcha)
    return captcha
def isLogin():
    #通过查看个人用户信息来判断
    url="https://www.zhihu.com/settings/profile"
    login_code=session.get(url,headers=headers,allow_redirects=False).status_code
    if login_code==200:
        return True
    else:
        return False
def login(secret,account):
    #通过输入用户名来判断是否是手机号码
    if re.match(r"^1\d{10}$",account):
        print('手机号码登录\n')
        post_url="https://www.zhihu.com/settings/profile"
        post_data={
            '_xsrf':get_xsrf(),
            'password':secret,
            'remember_me':True,
            'email':account
        }
    else:
        if '@' in account:
            print('邮箱登录\n')
        else:
            print('你输入的账号有问题，请重新登录')
            return 0
        post_url='http://www.zhihu.com/login/email'
        post_data = {
            '_xsrf': get_xsrf(),
            'password': secret,
            'remember_me': True,
            'email': account
        }
    try:
        #不要验证码直接登录
        login_page=session.post(post_url,data=post_data,headers=headers)
        login_code=login_page.text
        print(login_page.status_code)
        print(login_code)
    except:
        #需要输入验证码登录
        postdata['captcha']=get_captcha()
        login_page=session.post(post_url,data=post_data,headers=headers)
        login_code=eval(login_page.text)
        print(login_code['msg'])
    session.cookies.save()

if __name__=='__main__':
    if isLogin():
        print('您已经登录')
    else:
        account = input('请输入你的用户名\n>  ')
        secret = input("请输入你的密码\n>  ")
        login(secret,account)

