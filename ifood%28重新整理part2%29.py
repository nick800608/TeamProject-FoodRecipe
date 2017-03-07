
# coding: utf-8

# In[82]:

import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import traceback as tb
import json


# In[83]:

###上層


url = 'https://ifoodie.tw/search'

driver = webdriver.PhantomJS(executable_path=r'C:\Users\user\Desktop\phantomjs-2.1.1-windows\bin\phantomjs.exe')  # PhantomJS
driver.get(url)  # 把網址交給瀏覽器 
pageSource = driver.page_source  # 取得網頁原始碼
soup = BeautifulSoup(pageSource, 'lxml')  # 解析器接手


data = soup.find("a", {"class":"ng-binding"})
data1 =soup.select("a.ng-binding")
for tag in data:
    href= data.get("href")
    url = 'https://ifoodie.tw{}'.format(href).strip()
    print(url)
    
    next_crawler(url)
#==============================================================================================================================
def next_crawler(url):
    ### 中層   


    # Example:茶寮侘助,餐廳外部資訊,有些東西是我們所要的
    url = 'https://ifoodie.tw/blog/58bcd12b699b6e645195f4f3-漂丿燒肉食堂'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'lxml')

    mydict={}
    #熱門指數
    hot_soup = soup.select("#ratingStar > span")
    for hot in hot_soup:
        熱門指數 = hot.text.strip()
    mydict['熱門指數'] = 熱門指數

    #餐廳評分
    r_rate = soup.select("span.rating.rating4")
    mydict['rating'] = r_rate[0].text

    #作者
    author_name = soup.select("a.name")
    author_name = author_name[0].text
    mydict['author_name'] = author_name

    #作者 url
    author_url = soup.find("a", {"class":"name"})
    author_url = author_url.get("href")
    mydict['author_url'] = author_url

    # 標籤 再做細部處理==>去掉旁邊的html標籤
    tag_list=[]
    tag = soup.find_all("a", {"rel":"tag"})
    tag 
    # tag_lists = tag_list.append(tag)
    mydict['tag']=tag

    #觀看人數
    see_soup = soup.select("div.stat")
    see_soup = see_soup[0].text
    mydict['see']=see_soup

    #餐廳電話號碼
    phone_number = soup.select("div.phone.right")[0].text.split(":")[1]
    phone_number
    mydict['phone_number'] = phone_number
    #超連結
    url = soup.find("a", {"href":"/restaurant/58bda5762756dd732889b47d"})
    url= url.get("href")
    url2 = 'https://ifoodie.tw'+url
    mydict['web_url'] = url2
    mydict
    
    return mydict
    final_crawler(url2)
    
#=============================================================================================================================
### 下層 
def final_crawler(url2):

    # Example:茶寮侘助,餐廳外部資訊,有些東西是我們所要的

    res = requests.get("https://ifoodie.tw/restaurant/559bc6aec03a101f6d8b5fc2")
    soup = BeautifulSoup(res.text, 'lxml')


    #營業時間
    mydict={}
    reup = soup.select("span.info_detail")
    mydict['address']=reup[0].text
    mydict['opentime']=reup[1].text
    mydict['avg_consume']=reup[2].text

    #餐廳名字
    restaurant_name = soup.select("h1.title")[0]
    restaurant_name=restaurant_name.text
    mydict['restaurant_name']=restaurant_name
    #餐廳分類
    reup1 = soup.select("a.info_detail")

    for tag1 in reup1:
        tag1=tag1.text
    mydict['category']=tag1

    #訪客言談 細部處理 去掉旁邊的html標籤

    message = soup.find_all("div", {"itemprop":"description"})
    message = message 

    mydict['message:']=message
    mydict
    print(mydict)
    return mydict


# In[ ]:

def next_crawler(url):
    ### 中層   
    import requests
    import traceback as tb
    import json
    from bs4 import BeautifulSoup

    # Example:茶寮侘助,餐廳外部資訊,有些東西是我們所要的
    url = 'https://ifoodie.tw/blog/58bcd12b699b6e645195f4f3-漂丿燒肉食堂'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'lxml')

    mydict={}
    #熱門指數
    hot_soup = soup.select("#ratingStar > span")
    for hot in hot_soup:
        熱門指數 = hot.text.strip()
    mydict['熱門指數'] = 熱門指數

    #餐廳評分
    r_rate = soup.select("span.rating.rating4")
    mydict['rating'] = r_rate[0].text

    #作者
    author_name = soup.select("a.name")
    author_name = author_name[0].text
    mydict['author_name'] = author_name

    #作者 url
    author_url = soup.find("a", {"class":"name"})
    author_url = author_url.get("href")
    mydict['author_url'] = author_url

    # 標籤 再做細部處理==>去掉旁邊的html標籤
    tag_list=[]
    tag = soup.find_all("a", {"rel":"tag"})
    tag 
    # tag_lists = tag_list.append(tag)
    mydict['tag']=tag

    #觀看人數
    see_soup = soup.select("div.stat")
    see_soup = see_soup[0].text
    mydict['see']=see_soup

    #餐廳電話號碼
    phone_number = soup.select("div.phone.right")[0].text.split(":")[1]
    phone_number
    mydict['phone_number'] = phone_number
    #超連結
    url = soup.find("a", {"href":"/restaurant/58bda5762756dd732889b47d"})
    url= url.get("href")
    url2 = 'https://ifoodie.tw'+url
    mydict['web_url'] = url2
    mydict

    final_crawler(url2)


# In[ ]:

### 下層 
def final_crawler(url2):
    import requests
    import traceback as tb
    import json
    from bs4 import BeautifulSoup


    # Example:茶寮侘助,餐廳外部資訊,有些東西是我們所要的

    res = requests.get("https://ifoodie.tw/restaurant/559bc6aec03a101f6d8b5fc2")
    soup = BeautifulSoup(res.text, 'lxml')


    #營業時間
    mydict={}
    reup = soup.select("span.info_detail")
    mydict['address']=reup[0].text
    mydict['opentime']=reup[1].text
    mydict['avg_consume']=reup[2].text

    #餐廳名字
    restaurant_name = soup.select("h1.title")[0]
    restaurant_name=restaurant_name.text
    mydict['restaurant_name']=restaurant_name
    #餐廳分類
    reup1 = soup.select("a.info_detail")

    for tag1 in reup1:
        tag1=tag1.text
    mydict['category']=tag1

    #訪客言談 細部處理 去掉旁邊的html標籤

    message = soup.find_all("div", {"itemprop":"description"})
    message = message 

    mydict['message:']=message
    mydict


# In[136]:




# In[ ]:



