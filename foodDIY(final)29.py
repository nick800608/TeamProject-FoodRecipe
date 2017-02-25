
# coding: utf-8

# In[4]:

from collections import OrderedDict as od
import json
import csv
import traceback as tb            
import requests
import re #import 正規表示法相關模組
from bs4 import BeautifulSoup

# HOSt="http://www.ttv.com.tw/"



# In[11]:

def page_crawler(no_pages):#算美食DIY 總頁數
    
#     HOSt="http://www.ttv.com.tw/"
    

    res = requests.get("http://www.ttv.com.tw/cuisine/Search.aspx?lnk=tag&val=hotrecipe&page=1")
    soup = BeautifulSoup(res.text, 'lxml')
    total_page=int(soup.select("#ctl00_cph1_pagingResult_pnlPaging")[0].select('#ctl00_cph1_pagingResult_lblPageCount')[0].text)
    #total_page=總頁數  每頁15道菜
    for page in range(1, no_pages+1, +1):
        url = "http://www.ttv.com.tw/cuisine/Search.aspx?lnk=tag&val=hotrecipe&page={}".format(page)
        print(url)
        
        list_crawler(url)#呼叫下一頁 的list爬蟲幫忙
#===============================================================================================================================        
def list_crawler(url):
    res1 = requests.get(url)
    soup1 = BeautifulSoup(res1.text, 'lxml')
    
    article_list=[]
    for tag in soup1.select('h3.style3.ftitle.wrap > a'):
        title = tag.text
        url1 = tag['href'].split("=")[1]#取得內文頁的index

        url2 = "http://www.ttv.com.tw/cuisine/Detail2.aspx?rid={}".format(url1)#內文頁的url
        print(url2)
        article_crawler(url2)#呼叫下一個article 內文頁爬蟲
#===============================================================================================================================       
def article_crawler(url2):

    import requests
    from bs4 import BeautifulSoup
    import traceback
   
    fooddiy_article_url = url2
    
    res = requests.get(fooddiy_article_url)
    soup = BeautifulSoup(res.text, 'lxml')
    
    mydict={} 
    for tag1 in soup.select(" .videoblock > .c490bgline > .c490con > .style15.fl.wrap"):#食譜名稱
        title=tag1.text
    mydict["title"]=title
    
    reup = soup.select(" #fcontent ")[0]#食材和步驟中間都是 id=fcontent,下面的標籤就只有 class x了先給他一個變數,這樣好分辨
    #爬的量一大時會有Error Message:list index out of range 在 reup = soup.select(" #fcontent ")[0]
       
    foodName = reup.select(" .style11 ")[0]
    foodName = foodName.text
    mydict["foodName"]=foodName

    
#   人氣

    rreup = soup.select(" #faction")[0]
    foodPeople = rreup.select(" .style6")[0]
    foodPeople = foodPeople.text
    
    mydict["foodPeople"]=foodPeople

#食材步驟
    foodStep = reup.select(" .style11 ")[1]
    foodStep = foodStep.text

    mydict["foodStep"]=foodStep
    
    print(mydict)       


# In[12]:

page_crawler(2)  #example: 爬兩頁 的每道食譜內容


# In[13]:

import os   #建目錄確認之前是否有存在

dir = "foodDiy_final"
if not os.path.exists(dir):
    os.mkdir(dir)
else:
    print(dir+"檔案已經建立了!!")


# In[14]:

with open('./foodDiy_final.txt','w') as f:
    f.write(str(mydict)) 
    print("檔案以寫入")
    f.close()


# In[15]:

content='''
Welcome to foodDIY
'''
with open('foodDiy_final.txt','w') as f:
    f.write(content) 
    print("檔案以寫入")
    f.close()


# In[13]:

def list_crawler(url):
    res1 = requests.get(url)
    soup1 = BeautifulSoup(res1.text, 'lxml')
    for tag in soup1.select('h3.style3 ftitle wrap > a'):
        title = tag.text
        url1 = tag['href'].split("=")[1]#取得內文頁的index
        url2 = HOST + "cuisine/Detail2.aspx?rid={}".format(url1)#內文頁的url
        print(url2)
        article_crawler(url2)#呼叫下一個article 內文頁爬蟲


# In[14]:

def article_crawler(url2):

    import requests
    from bs4 import BeautifulSoup
    import traceback
   
    fooddiy_article_url = url2
    
    res = requests.get(fooddiy_article_url)
    soup = BeautifulSoup(res.text, 'lxml')
    
    mydict={} 
    for tag1 in soup.select(" .videoblock > .c490bgline > .c490con > .style15.fl.wrap"):#食譜名稱
        title=tag1.text
    mydict["title"]=title
    
    reup = soup.select(" #fcontent ")[0]#食材和步驟中間都是 id=fcontent,下面的標籤就只有 class x了先給他一個變數,這樣好分辨
    #爬的量一大時會有Error Message:list index out of range 在 reup = soup.select(" #fcontent ")[0]
       
    foodName = reup.select(" .style11 ")[0]
    foodName = foodName.text
    mydict["foodName"]=foodName

    
#   人氣

    rreup = soup.select(" #faction")[0]
    foodPeople = rreup.select(" .style6")[0]
    foodPeople = foodPeople.text
    
    mydict["foodPeople"]=foodPeople

#食材步驟
    foodStep = reup.select(" .style11 ")[1]
    foodStep = foodStep.text

    mydict["foodStep"]=foodStep
    
    print(mydict)


# In[15]:

page_crawler(6)


# In[ ]:



