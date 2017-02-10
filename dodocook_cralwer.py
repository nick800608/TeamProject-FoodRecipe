
# coding: utf-8

# In[ ]:




# In[29]:

#起始標準起手式~
import requests as rq
from bs4 import BeautifulSoup as bs
from collections import OrderedDict as od
import json
import csv
import traceback as tb
import re    


# In[30]:

HOST = 'http://www.dodocook.com/recipe/'


# In[31]:

#def dodocook_crawler(開始文章ID,結束文章ID)
def dodocook_crawler(no_start_page,no_stop_page):
    HOST = 'http://www.dodocook.com/recipe/'
    #在pass這裡接上function() 網址產生器
    #pass
    url_builder(HOST,no_start_page,no_stop_page)
    


# In[32]:

#網址產生器
#url_builder(網站URL, 開始文章ID, 結束文章ID)
def url_builder(HOST,no_start_page,no_stop_page):
    for i in range(no_start_page, no_stop_page):
        url = HOST + "{}/".format(i)        
        print("[INFO] {}".format(url))
        #在pass這裡接上function()  res_and_soup(url)
        #pass
        res_and_soup(url)


# In[33]:

#就字面意思
def res_and_soup(url):
    try:
        res = rq.get(url)
        soup = bs(res.text, 'lxml')
        print("[INFO] success")
        #在pass這裡接上爬取網頁內容的function()
        #pass
        dodocook_contents(soup)
    except:
        print("[Error] Error while getting contents")
        tb.print_exc()


# In[34]:

def dodocook_contents(soup):
    #title
    mydict={}
    for tag1 in soup.select(".band > h1"):
        title=tag1.text
    mydict["title"]=title
        
    #foodname
    foodName=[]
    for tag2 in soup.select(".body > .list > .name"):
        tag2_dict={}
        n=soup.select(".body > .list > .name").index(tag2)
        tag2_dict[tag2.text]=soup.select(".ingredient > .body > .list > .count")[n].text
        foodName.append(tag2_dict)
    mydict["foodName"]=foodName
    
    #step
    step1=[]
    step_list1=soup.select('.steps > .CSrtB > .Sno') 
    step_go1=soup.select('.steps > .CSrtB > .SBpma')

#     step2=[] 
#     step_list2=soup.select('.steps > .CSrtA > .SrtAk > .Sno') 
#     for tag3 in step_list2:
#         print(tag3.text)
#     step_go2=soup.select('.steps > .CSrtA > .SrtAk > .Spma > p')
#     for tag4 in step_go2:
#         print(tag4.text)
        
    
    for tag3 in step_list1:
        tag3_dict={}
        n1=step_list1.index(tag3)
        tag3_dict[tag3.text]=step_go1[n1].text
        step1.append(tag3_dict)
    mydict["step"]=step1
    print(mydict)


# In[35]:

dodocook_crawler(40000,40010)


# In[ ]:



