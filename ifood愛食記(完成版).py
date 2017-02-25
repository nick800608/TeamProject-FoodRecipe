
# coding: utf-8

# ##### 這是第一頁的爬蟲

# In[19]:

import requests
from operator import itemgetter
import traceback as tb
import json
#這是爬第一頁餐廳20筆資料的相關內容      因為第一頁的url 我用.format()抓不到東西  所以在這我分第一頁 和 第二頁以後來分開爬蟲
for k in range(0,20):
    url = "https://ifoodie.tw/api/blog/?order_by=-date"
    res=requests.get(url).json()

    try:    
        res_info = res['response'][k]#先訂大括號的 標籤屬性
        #         print(res_info)

        restotal={}
        restaurant_info=[]
        restaurant_info_detail={}

                #店家名稱
        restaurant_name = res_info['restaurant']['name']
        restaurant_info_detail["restaurant_name:"]=restaurant_name#先塞到restaurant_info_detail字典裡面




                #營業時間
        open_time = res_info['restaurant']['opening_hours']
        restaurant_info_detail["open_time"]=open_time#先塞到restaurant_info_detail字典裡面



                #地點
        restaurant_location=res_info['restaurant']['address']
        restaurant_info_detail["restaurant_location:"]=restaurant_location#先塞到restaurant_info_detail字典裡面



                #連絡電話
        phone_number=res_info['restaurant']['phone']
        restaurant_info_detail["phone_number"]=phone_number#先塞到restaurant_info_detail字典裡面
        restaurant_info.append(restaurant_info_detail)
    #             restotal["phone_number:"]=phone_number
            
            
                #把以上四個資訊裝到字典裡

        restotal["restaurant_info:"]=restaurant_info

                #圖片
        img_url=res_info['restaurant']['cover_url']
        restotal["img_url:"]=img_url


                # #網址
        web_url=res_info['url']
        restotal["web_url:"]=web_url
        print(restotal)
    except :
        print("[Error] Error while getting contents")
        tb.print_exc()


# In[ ]:




# ##### 這是第二頁以後的爬蟲
# 

# In[15]:

#起頭式   以下是第二頁以後的爬蟲
import csv
import requests
from operator import itemgetter
import traceback as tb
import json
from bs4 import BeautifulSoup


# In[16]:

def page_url(no_pages):
    for page in range(1*20, (no_pages+1)*20, 20):
        url = "https://ifoodie.tw/api/blog/?offset={}&limit=20&order_by=-date".format(i)
        print(url)
        
        list_incontent(url)#呼叫下一頁 的list_incontent爬蟲幫忙


# In[17]:

def list_incontent(url):
    res1 = requests.get(url)
    soup1 = BeautifulSoup(res1.text, 'lxml')  
    
    for j in range(0,20):#第0,1頁的內文頁爬蟲
        
        res_info = res['response'][j]#先訂大括號的 標籤屬性
#         print(res_info)
        
        try:
            restotal={}
            restaurant_info=[]
            restaurant_info_detail={}
            
            #店家名稱
            restaurant_name = res_info['restaurant']['name']#取得 restaurant_name
            restaurant_info_detail["restaurant_name"]=restaurant_name#先塞到restaurant_info_detail字典裡面

#             restotal["restaurant_name:"]=restaurant_name
            

            #營業時間
            open_time = res_info['restaurant']['opening_hours']#取得open_time
            restaurant_info_detail["open_time"]=open_time#先塞到restaurant_info_detail字典裡面

#             restotal["open_time:"]=open_time
           

            #地點
            restaurant_location=res_info['restaurant']['address']#取得restaurant_location
            restaurant_info_detail["restaurant_location"]=restaurant_location#先塞到restaurant_info_detail字典裡面

#             restotal["restaurant_location:"]=restaurant_location
          

            #連絡電話, 在想說要不要用正規表達時來抓取,但是觀察很久只有一筆是8位數個電話號碼,其他都是 ex:0989360910這種格式
            phone_number=res_info['restaurant']['phone']#取得phone_number
            restaurant_info_detail["phone_number"]=phone_number#先塞到restaurant_info_detail字典裡面
            restaurant_info.append(restaurant_info_detail)
#             restotal["phone_number:"]=phone_number
            
            
            #把以上四個資訊裝到字典裡

            restotal["restaurant_info:"]=restaurant_info

            #圖片
            img_url=res_info['restaurant']['cover_url']#取得圖片
            restotal["img_url:"]=img_url#塞到字典
           

            # #網址
            web_url=res_info['url']#取得網址
            restotal["web_url:"]=web_url
            print(restotal)
        except TypeError:
            print("[Error Message] Error while getting contents")
            tb.print_exc()    


# In[18]:

page_url(1) #自己DIY 要爬幾頁的內容  #爬取下一頁以上的資料


# In[ ]:




  

