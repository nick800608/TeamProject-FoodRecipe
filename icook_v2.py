# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 19:21:37 2017

@author: Owner
"""

import requests
from bs4 import BeautifulSoup
from pymongo import *
import threading    #導入 threading 模組
from multiprocessing import Queue

HOST = 'https://icook.tw/recipes/'

def icook_crawler(q):
    # while soup.find('h1').text.strip()!="唉啊! 這個頁面不見了": 如何在爬資料時使電腦知道這個網頁是不用爬的? 
    
    
    
    for i in range(20000,20010):

        url=HOST+"{}".format(i)
        res = requests.get(url)
        res.encoding="utf-8"
        soup = BeautifulSoup(res.text, 'lxml')
        
        
        total_list=[]
        #先判斷裡面是不是有效的網頁
        try:
            test = soup.find('h1').text
            if not "唉啊" in test:
                #print("test")

                #建立存放icook食譜的空字典
                mydict={}

                #存進各食譜的的食譜名稱
                title = soup.select('h1')[0].text.strip()
                mydict['title']=title

                #存進各食譜的簡單敘述，這邊修改成一個list因為有的裡面有很多不同的敘述
                description=[]
                desc_list = soup.select('.recipe-description > div > p')
                for desc in desc_list:
                    descs = desc.text.strip()
                    description.append(descs)    
                mydict['description'] = description  

                #食材的存取，還需要修改!!!!!!
                ingredients=[]
                ing_list=soup.select('.ingredient-name')

                for ing in ing_list:
                    ing_dict={}

                    n = ing_list.index(ing)
                    ing_dict[ing.text.strip()] = soup.select('.ingredient-unit')[n].text.strip()
                    ingredients.append(ing_dict)


                mydict['ingredients']=ingredients
                # print(mydict)

                #製作食譜的步驟，用一個list來存取
                steps=[]
                step_list = soup.select('.media-body > big')
                # print(step_list)
                for step in step_list:
                    n = step_list.index(step)
                    step.extract()
                    s = soup.select('.media-body')[n].text.strip().replace(" ",'')
                    steps.append(s)

                mydict['steps']=steps

                #存進webURL
                mydict["webURL"] = url

                #取得圖片在class=main-pic的src屬性(url)
                image=soup.find('img',{'class':'main-pic'}).get("src")
                mydict['imageURL'] = image

                tips=[]    
                for text in soup.find_all("div", {"class":"notes"}):
                    tips=text.get_text().replace("\n","").replace("小撇步","") 

                mydict['tips']=tips  

                #收藏人數
                for liked in soup.select('div.meta > span.recipe-favorites'):
                    #print(liked.get_text())
                    mydict['liked']=liked.get_text().replace("\n","").strip()

                #瀏覽人數
                for read in soup.select('div.meta-bottom > span.count-tooltip'):
                    #print(read.get_text())
                    mydict['read']=read.get_text().replace("\n","").replace("瀏覽","").strip()

                #發表日期
                for date in soup.select('div.meta-bottom > span.timestamp'):
                    #print(date.get_text())
                    mydict['date']=date.get_text().replace("\n","").replace("發表","").strip()

                #total_list.append(mydict)
                #v把資料寫進mongodb
                client = MongoClient("mongodb://localhost:27017/")
                db = client['test']
                collect = db['test1']
                collect.insert_one(mydict)

                #print(mydict)

                q.put(mydict)
        except IndexError:
            print('[ERROR] : empty page!')
             
if __name__ == '__main__': 
    #lock = threading.Lock()  #命名一個 Lock 物件
    q = Queue() # 開一個 Queue 物件
    t1 = threading.Thread(target=icook_crawler, args=(q,)) 
                            #打開一個名字叫 t1 的線程物件
                            #這個物件會去呼叫 job1
                            #同時t1導入 q 跟 lock 做現成控制
                            

    t1.start()  #啟動 t1 線程
    
    t1.join()  #在 t1線程結束前阻止程式繼續運行
    

#確認Queue是否為空，如果不是就用 q.get() 取出值
    while not q.empty():   
        print(q.get())
    

#確認Queue是否為空，如果不是就用 q.get() 取出值
    #while not q.empty():   
    print(q.get())        