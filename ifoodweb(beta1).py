
# coding: utf-8

# In[5]:

import csv
import requests
import json
import traceback as tb

#第20 ==> 以上的餐廳 內容

#url ==>https://ifoodie.tw/api/blog/?offset=20&limit=20&order_by=-date
for i in range(20,40,20):
    url = "https://ifoodie.tw/api/blog/?offset={}&limit=20&order_by=-date".format(i)
    res=requests.get(url).json()
   
    #現在是抓20,40,60,80 的第0頁
    #第0個餐廳的所有資訊
    #餐廳資訊
    for j in range(0,10):
        
        res_info = res['response'][j]
#         print(res_info)
        
        try:
            
            restaurant_info={}
            restaurant_info_detail=[]
            
            #店家名稱
            restaurant_name = res_info['restaurant']['name']
            restaurant_info_detail.append(restaurant_name)
            restaurant_info["restaurant_name:"]=restaurant_name
            # print(res)

            #營業時間
            open_time = res_info['restaurant']['opening_hours']
            restaurant_info_detail.append(open_time)
            restaurant_info["open_time:"]=open_time
            # print(res)

            #地點
            restaurant_location=res_info['restaurant']['address']
            restaurant_info_detail.append(restaurant_location)
            restaurant_info["restaurant_location:"]=restaurant_location
            # print(res)

            #連絡電話
            phone_number=res_info['restaurant']['phone']
            restaurant_info_detail.append(phone_number)
            restaurant_info["phone_number:"]=phone_number
            # print(res)

            #圖片
            img_url=res_info['restaurant']['cover_url']
            restaurant_info["img_url:"]=img_url
            # print(res)

            # #網址
            web_url=res_info['url']
            restaurant_info["web_url"]=web_url
            print(restaurant_info)
        except :
            print("[Error] Error while getting contents")
            tb.print_exc()


#==================================================================================================================================

    #第0 ==>20的餐廳 內容
url = "https://ifoodie.tw/api/blog/?order_by=-date"
res=requests.get(url).json()
   
    #現在是抓20,40,60,80 的第0頁
    #第0個餐廳的所有資訊
    #餐廳資訊
for j in range(0,20):
    res_info = res['response'][j]
#     print(res_info)


    try:
        restaurant_info={}
        restaurant_name = res_info['restaurant']['name']
        restaurant_info["restaurant_name:"]=restaurant_name
        # print(restaurant_info)

        #營業時間
        open_time = res_info['restaurant']['opening_hours']
        restaurant_info["open_time:"]=open_time
        # print(restaurant_info)

        #地點
        restaurant_location=res_info['restaurant']['address']
        restaurant_info["restaurant_location:"]=restaurant_location
        # print(restaurant_info)

         #連絡電話
        phone_number=res_info['restaurant']['phone']
        restaurant_info["phone_number:"]=phone_number
        # print(restaurant_info)

        #圖片
        img_url=res_info['restaurant']['cover_url']
        restaurant_info["img_url:"]=img_url
        # print(restaurant_info)

        # #網址
        web_url=res_info['url']
        restaurant_info["web_url"]=web_url
        print(restaurant_info)
    except :
        print("[Error] Error while getting contents")
        tb.print_exc()







