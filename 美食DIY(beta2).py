
# coding: utf-8

# In[1]:

from collections import OrderedDict as od
import json
import csv
import traceback as tb            
import requests
import re #import 正規表示法相關模組
from bs4 import BeautifulSoup
res = requests.get("http://www.ttv.com.tw/cuisine/Search.aspx?lnk=tag&val=hotrecipe&page=1")
res.encoding = 'utf-8'
soup = BeautifulSoup(res.text.encode('utf-8'))
pagenum = int(soup.select('#ctl00_cph1_pagingResult_pnlPaging')[0].select('#ctl00_cph1_pagingResult_lblPageCount')[0].text.encode('utf-8').strip())
print (pagenum)#算總頁數 為了方便計算 change==> int ,觀察頁面得知每頁有15道菜
total_pagenum=pagenum*15
print(total_pagenum)#得知食譜總共有2115道菜


# In[2]:

import requests
from bs4 import BeautifulSoup

for i in range(1,100):
    url = 'http://www.ttv.com.tw/cuisine/Detail2.aspx?rid={}'.format(i)
# url = 'http://www.ttv.com.tw/cuisine/Detail2.aspx?rid=1980'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'lxml')


# In[3]:

mydict={} #食譜名稱
title = soup.select(" .videoblock > .c490bgline > .c490con > .style15.fl.wrap")
print(title)
mydict["title"]=title


# In[4]:

#最上層的標籤先固定好
reup = soup.select(" #fcontent ")[0]


# In[5]:

#食材名稱
foodName = reup.select(" .style11 ")[0]
print(foodName)
mydict["foodName"]=foodName


# In[ ]:

#食材步驟
foodStep = reup.select(" .style11 ")[1]
print(foodStep)
mydict["foodStep"]=foodStep

