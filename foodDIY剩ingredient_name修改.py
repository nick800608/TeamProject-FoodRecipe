
# coding: utf-8

# #### 起頭式預先import相關套件
# 

# In[5]:

from collections import OrderedDict as od
import json
import csv
import traceback as tb            
import requests
import re #import 正規表示法相關模組
from bs4 import BeautifulSoup
import os


# ##### 在這我分為總頁數爬蟲,,每頁的每筆url爬蟲,每筆內容爬蟲
# 

# In[21]:



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
    ingredients_main=[]
    ingredients_main_dict={}
    for tag1 in soup.select(" .videoblock > .c490bgline > .c490con > .style15.fl.wrap"):#食譜名稱
        recipe_name=tag1.text.strip()
    mydict["recipe_name:"]=recipe_name#recipe_name塞到dict裡
    
    reup = soup.select(" #fcontent ")[0]#食材和步驟中間都是 id=fcontent,下面的標籤就只有 class x了先給他一個變數,這樣好分辨
    
       
#     ingredient_name = reup.select(" .style11 ")[0].text
#     ingredient_name = ingredient_name.split()
    for tag2 in soup.select(" .style11 "):
        ingredient_name=tag2.split().text
    print(ingredient_name)#知道這道食材名稱是裝在list裡面
    
    ingredients_main_dict["ingredient_name:"]=ingredient_name#ingredient_name裝到字典裡
    ingredients_main.append(ingredients_main_dict)#加到字串中
    mydict["ingredients_main:"]=ingredient_name#加到字典裡

    
#   人氣

    rreup = soup.select(" #faction")[0]
    popularity = rreup.select(" .style6")[0]
    popularity = popularity.text.strip()
    
    mydict["popularity:"]=popularity

#食材步驟
    steps = reup.select(" .style11 ")[1]
    steps = steps.text.strip()

    mydict["steps:"]=steps
    
    print(mydict)       
    
    
    with open('food.json', 'w', encoding='utf-8') as fp:
        json.dump(mydict, fp, ensure_ascii=False)
        fp.close()
        
        
        
       

    #把資料寫到檔案裏面                        

 
 #exam
# try:
#     with open('C:\\Users\\' + os.getlogin() + '\\Desktop\\aaa.txt', 'w') as tmp:
#         tmp.write(kkk)
# except IOError as err:
#     print (err)
# finally:
#     tmp.close()

      
  


# In[22]:

page_crawler(1)  #example: 爬兩頁的每道食譜內容


# In[36]:


    
with open('food.json', 'w', encoding='utf-8') as fp:
    res = requests.get("http://www.ttv.com.tw/cuisine/Search.aspx?lnk=tag&val=hotrecipe&page=1")
    soup = BeautifulSoup(res.text, 'lxml')
    total_page=int(soup.select("#ctl00_cph1_pagingResult_pnlPaging")[0].select('#ctl00_cph1_pagingResult_lblPageCount')[0].text)
    #total_page=總頁數  每頁15道菜
    for page in range(1,total_page, +1):
        url = "http://www.ttv.com.tw/cuisine/Search.aspx?lnk=tag&val=hotrecipe&page={}".format(page)
        print(url)
    
        json_str = json.dump(url, fp, ensure_ascii=False)
        


# In[70]:

data = {}
data ['key1'] = "keyinfo"
data ['key2'] = "keyinfo2"  
data ['key1'] = "keyinfo"
data ['key2'] = "keyinfo2" 
data ['key1'] = "keyinfo"
data ['key2'] = "keyinfo2" 
data ['key1'] = "keyinfo"
data ['key2'] = "keyinfo2" 
data ['key1'] = "keyinfo"
data ['key2'] = "keyinfo2" 
data ['key1'] = "keyinfo"
data ['key2'] = "keyinfo2" 
data ['key1'] = "keyinfo"
data ['key2'] = "keyinfo2" 
data ['key1'] = "keyinfo"
data ['key2'] = "keyinfo2" 
data ['key1'] = "keyinfo"
data ['key2'] = "keyinfo2" 
data ['key1'] = "keyinfo"
data ['key2'] = "keyinfo2" 


# In[71]:

import json
with open('data.json', 'w') as fp:
    json.dump(data, fp)


# In[5]:

f = open('workfile', 'w')
print (f)


# In[24]:


    


# In[17]:




# In[ ]:



