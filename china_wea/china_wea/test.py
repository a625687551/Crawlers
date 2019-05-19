import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
import urllib
import hashlib
from bs4 import BeautifulSoup
import json
import os
import time
import datetime
# from mpl_toolkits import basemap
# myak='DhzUPOCzgD3zrfRChfombTGZh59v9fGG'
# url = 'http://api.map.baidu.com/geocoder/v2/?address={}&output=json&ak=DhzUPOCzgD3zrfRChfombTGZh59v9fGG'
# s=requests.get(url.format('北京'))
# print(s.json())
n=datetime.datetime.now()
s=os.stat(r'D:\学习\GitHub\china_wea\wea.txt').st_mtime
print(datetime.timedelta(n,s))