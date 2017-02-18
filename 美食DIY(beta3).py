
# coding: utf-8

# In[10]:

# from collections import OrderedDict as od
# import json
# import csv
# import traceback as tb            
# import requests
# import re #import 正規表示法相關模組
# from bs4 import BeautifulSoup
# res = requests.get("http://www.ttv.com.tw/cuisine/Search.aspx?lnk=tag&val=hotrecipe&page=1")
# res.encoding = 'utf-8'
# soup = BeautifulSoup(res.text.encode('utf-8'))
# pagenum = int(soup.select('#ctl00_cph1_pagingResult_pnlPaging')[0].select('#ctl00_cph1_pagingResult_lblPageCount')[0].text.encode('utf-8').strip())
# print (pagenum)#算總頁數 為了方便計算 change==> int ,觀察頁面得知每頁有15道菜
# total_pagenum=pagenum*15
# print(total_pagenum)#得知食譜總共有2115道菜

import requests
from bs4 import BeautifulSoup
import traceback
import re
for i in range(1,10):
    url = 'http://www.ttv.com.tw/cuisine/Detail2.aspx?rid={}'.format(i)
#     url = 'http://www.ttv.com.tw/cuisine/Detail2.aspx?rid=1980'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'lxml')
    
#     print(soup)
    
    mydict={} #食譜名稱
#     title = soup.select(" .videoblock > .c490bgline > .c490con > .style15.fl.wrap")
    for tag1 in soup.select(" .videoblock > .c490bgline > .c490con > .style15.fl.wrap"):
        title=tag1.text
    print(title)
    mydict["title"]=title
    
    reup = soup.select(" #fcontent ")[0]#食材和步驟中間都是 id=fcontent先給他一個變數,這樣好分辨
    #爬的量一大時會有Error Message:list index out of range 在 reup = soup.select(" #fcontent ")[0]

    
    foodName = reup.select(" .style11 ")[0]
# for tag2 in soup.select(" #fcontent > .style11 ")[0]:
# foodName=tag2.text.strip()
    foodName = foodName.text
    print(foodName)
    mydict["foodName"]=foodName
    
#食材步驟
    foodStep = reup.select(" .style11 ")[1]
# for tag3 in soup.select(" #fcontent > .style11 ")[1]:
#     foodStep = tag3.text.strip()
    foodStep = foodStep.text
    print(foodStep)
    mydict["foodStep"]=foodStep
print(mydict)


# In[ ]:



