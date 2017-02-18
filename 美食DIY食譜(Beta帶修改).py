
# coding: utf-8

# In[5]:

#我的美食DIY

from collections import OrderedDict as od
import json
import csv
import traceback as tb
import string               
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


# In[6]:

total=0

f='http://www.ttv.com.tw/cuisine/Search.aspx?lnk=tag&val=hotrecipe&page={0}'


# In[7]:

mydict = od()#排版順利用的
for page in range(1,pagenum+1):
    res = requests.get(f.format(page))
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text.encode('utf-8'),"lxml")
    
#     食譜網站連結的資訊不確定有需要爬下來嗎!  所以我先註解一下
#     for i in soup.select('.fcon'):#抓取食譜的網頁連結
#         tag = i.select('a')[0]['href']   
#         href = 'http://www.ttv.com.tw/cuisine/'+tag  #拚湊起來再開啟來check 一下      
# #         print (href)

        
#         res = requests.get(href)
#         res.encoding = 'utf-8'
#         soup = BeautifulSoup(res.text.encode('utf-8'))
#         print (soup)#把超連結用Beautiful包裝
        
        
        main = soup.select('.style15')[0].text#食材名稱 的class==>style15
        mydict["main"]=main #把食材裝在 mydict的字典裡
#         print ('name:'+ main +'\n')#印出食材名稱
        
        #打算nth-of-type子母選擇器來篩選
        name_materials = soup.select(" .style13")#印出材料,作法,小祕笈,書名,菜式別,國家別,出處
        mydict["name_materials"]=name_materials
#         print(name_materials)
        materials= soup.select(" .style11")#印出材料,作法,小祕笈 發現這三個東西的內容標籤是一樣的
        mydict["materials"]=materials
#         print(materials)

        
        #以下先做test
        practice = soup.select('ul')[0].select('.style11')[1].text
        practice_1=re.sub("\d\.", " ", practice) # practice_1是str    
        #practice_2=str.join(practice_1.split(' '),',')#"空白"轉換成","
        print ('practice:'+ practice_1 +'\n')

        
        total+=1
print (total)


# In[126]:

main = soup.select('.style15')[0].text#食材名稱 的class==>
print ('name:'+ main +'\n') 




# In[ ]:




# In[129]:




# In[63]:

type(materials)


# In[116]:

practice = soup.select('ul')[0].select('.style11')[1].text
practice



# In[106]:




# In[91]:

practice = soup.select('.style11')
practice


# In[124]:

type(practice_1)


# In[125]:

type(practice_2)


# In[15]:




# In[10]:




# In[ ]:




# In[13]:




# In[ ]:



