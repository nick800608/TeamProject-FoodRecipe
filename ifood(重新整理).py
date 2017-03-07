
# coding: utf-8

# In[4]:

###上層
import requests
from selenium import webdriver
from bs4 import BeautifulSoup

url = 'https://ifoodie.tw/search'

driver = webdriver.PhantomJS(executable_path=r'C:\Users\user\Desktop\phantomjs-2.1.1-windows\bin\phantomjs.exe')  # PhantomJS
driver.get(url)  # 把網址交給瀏覽器 
pageSource = driver.page_source  # 取得網頁原始碼
soup = BeautifulSoup(pageSource, 'lxml')  # 解析器接手

# tag = soup.select('div.media > div.media-body > div.title media-heading > a')
# url = "https://ifoodie.tw" +tag['href']
# print(url)
data = soup.find("a", {"class":"ng-binding"})
href= data.get("href")
url = 'https://ifoodie.tw{}'.format(href).strip()
print(url)
# url1 = 'https://ifoodie.tw'
# for tag in soup.select('a.ng-binding'):
#     url1 = HOST + tag['href']
#     print(url)


# In[30]:


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


#超連結
url = soup.find("a", {"href":"/restaurant/58bda5762756dd732889b47d"})
url= url.get("href")
url2 = 'https://ifoodie.tw'+url
mydict['web_url'] = url2
mydict
#呼叫內文爬從


# In[33]:

### 下層   
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
mydict['dollars']=reup[2].text


#餐廳分類
reup1 = soup.select("a.info_detail")
for tag1 in reup1:
     print(tag1.text)
mydict['分類']=tag1.text
    
#訪客言談 細部處理 去掉旁邊的html標籤
message = soup.find_all("div", {"itemprop":"description"})
message
mydict['message:']=message
mydict


# In[136]:




# In[ ]:



