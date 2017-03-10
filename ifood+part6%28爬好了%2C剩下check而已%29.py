
# coding: utf-8

# In[ ]:




# In[16]:

import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import traceback as tb
import json
# from pymongo import MongoClient

# In[83]:

###上層


url = 'https://ifoodie.tw/search'


# In[17]:



driver = webdriver.PhantomJS(executable_path=r'C:\Users\user\Desktop\phantomjs-2.1.1-windows\bin\phantomjs.exe')  # PhantomJS
driver.get(url)  # 把網址交給瀏覽器 
pageSource = driver.page_source  # 取得網頁原始碼
soup = BeautifulSoup(pageSource, 'lxml')  # 解析器接手


# In[18]:





def page_crawler(no_page):
    try:
        url1 = 'https://ifoodie.tw'
        for i in range(1,no_page+1,1):#一頁有20家爬蟲 這個例子應該有200家
            for tag in soup.select('div.blog-item-s.ng-scope > div.media > div.media-body > div.title.media-heading > a'):
                url_next = url1 + tag['href']
                print(url_next)
                next_crawler(url_next)#呼叫下一層的爬蟲
    except IndexError:
        print("finding error")
#====================================================================================================================


# In[19]:

def next_crawler(url_next):
    ### 中層   

    try:
    # Example:茶寮侘助,餐廳外部資訊,有些東西是我們所要的
#     url = 'https://ifoodie.tw/blog/58bcd12b699b6e645195f4f3-漂丿燒肉食堂'這行網址是練習用的,check時可忽略
        res = requests.get(url_next)
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
        
        #照片
        img_url = soup.select(".pull-left > .media-object.cover")
        img_url = img_url[0].get("style").split("(")[1].split(")")[0]
        mydict['img_url'] = img_url
#         print(img_url)
        
        # 標籤 再做細部處理==>去掉旁邊的html標籤
        tag_list=[]
        tags = soup.find_all("a", {"rel":"tag"})
        for tag in tags:
            tag = tag.text
            tag_list.append(tag)
            mydict['tag']=tag_list

        #觀看人數
        see_soup = soup.select("div.stat")
        see_soup = see_soup[0].text
        mydict['see']=see_soup

        #餐廳電話號碼
        phone_number = soup.select("div.phone.right")[0].text.split(":")[1]
        phone_number
        mydict['phone_number'] = phone_number
        #超連結
        url = soup.select("div.restaurant.item.right > h4 > a")
        url= url[0].get('href')
        

        url_final = 'https://ifoodie.tw{}'.format(url)
        mydict['web_url'] = url_final

        final_crawler(url_final,mydict)        
    except IndexError:
        pass


# In[20]:

def final_crawler(url_final,mydict):
    # Example:茶寮侘助,餐廳外部資訊,有些東西是我們所要的
    try:
        res = requests.get(url_final)
        soup = BeautifulSoup(res.text, 'lxml')


        #營業地址
        #mydict={}
        reup = soup.select("span.info_detail")
        #print(reup)
        mydict['address']=reup[0].text
            #營業時間
        mydict['opentime']=reup[1].text
            #均消
        mydict['avg_consume']=reup[2].text

            #餐廳名字
        restaurant_name = soup.select("h1.title")[0]
        restaurant_name=restaurant_name.text
        mydict['restaurant_name']=restaurant_name
            #餐廳分類
        reup1 = soup.select("a.info_detail")
        #print(reup1)
        for tag1 in reup1:
            tag1=tag1.text
            mydict['category']=tag1

        #訪客言談 細部處理 去掉旁邊的html標籤
        message_total=[]
        #人
        message_mans=soup.select('div.right_wrap > div.user_name > a')
        for message_man in message_mans:
            mydict['message_man']=message_man.text
           
        #時間
#         message_times=soup.select('div.info > meta')
#         for message_time in message_times:
#             mydict['message_time']=message_time.text
            #print(message_time)
        #留言
        message_list=[]
        messages = soup.select("div.message > div")
        for message in messages:
            message = message.text
            message_list.append(message)
            mydict['message'] = message_list

            
#         tag_list=[]
#         tags = soup.find_all("a", {"rel":"tag"})
#         for tag in tags:
#             tag = tag.text
#             tag_list.append(tag)
#             mydict['tag']=tag_list
        print(mydict)
#         goto_mongo(mydict) 
            
        
        
        
    except IndexError:
        print('sorry not catch the information')
 


    


# In[21]:

page_crawler(10)


# In[22]:

def goto_mongo(mydict):#要開啟 mongo的server能夠使用
    client = MongoClient()
    db= client['test']
    collect = db['test_ifood']
    #一次insert一整個list
    collect.insert_one(mydict)


# In[ ]:




# In[ ]:




# In[256]:




# In[219]:




# In[282]:




# In[277]:




# In[260]:




# In[261]:




# In[262]:




# In[263]:




# In[264]:




# In[265]:




# In[266]:




# In[267]:




# In[269]:


    


# In[135]:


    


# In[138]:




# In[139]:




# In[132]:




# In[ ]:



