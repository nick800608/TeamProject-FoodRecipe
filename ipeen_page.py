import requests as r
from bs4 import BeautifulSoup as bs
import json 
from queue import Queue
import threading
import re
import time
url_base = 'http://www.ipeen.com.tw'



#爬取愛評網各個縣市分類的餐廳評論頁數網址
def page_crawler(q):
#     city_list = ['keelung','taipei','xinbei','taoyuan','hsinchu','hsinchucounty','miaoli','taichung','nantou','changhua','yunlin','chiayi'
#                 ,'chiayicounty','tainan','kaohsiung','pintung','ilan','hualian','taitung','penghu','lianjiang','kinmen']



    #台灣餐廳評論的所有頁數從最新到最舊

    try:
        url = 'http://www.ipeen.com.tw/search/taiwan/000/1-0-0-0/'
        res = r.get(url)
        res.encoding="utf-8"
        soup = bs(res.text, 'lxml')
        page_url_list=[]
        #取得最後一頁的頁數
        finalpage = soup.select('.next_p_s > a')[0].get('href').split('=')[1]
        int_page = int(finalpage)
        for i in range(1,int_page+1):
            page_url = url+'?p={}'.format(i)

            print(page_url)
            q.put(page_url)
            #呼叫取得餐廳裡的所有評論網址的方法
            #all_restaurant_list(page_url)
    #避免遇到index error
    except IndexError:
        print("[ERROR] : index error!")
    #爬取所有餐廳list，並看該餐廳最大的評論數目
def all_restaurant_list(page_url):
    
    res = r.get(page_url)
    res.encoding="utf-8"
    soup = bs(res.text, 'lxml')


    time.sleep(1)
    #每頁最多有15個餐廳list
    last_list = soup.select('.serShop')[-1].select('h3')[0].get('id').split('_')[2]
    int_list = int(last_list)



    for i in range(1,int_list+1):
        try:
            #取到的是/shop/數字
            restaurant_num = soup.select('#shop_h3_{} > a'.format(i))[0].get('href').split('-')[0]

#             print(restaurant_num)

            #取得每間餐廳評論的最大數目
            restaurant_url = 'http://www.ipeen.com.tw/shop/{}/comments?p=1&sortway=d&so=shop_default'.format(restaurant_num.split('/')[2])
            res_r = r.get(restaurant_url)
            res_r.encoding="utf-8"
            soup_r = bs(res_r.text, 'lxml')
            gray_text = soup_r.select('.info > h1 > span')[0].text
            if "已歇業"not in gray_text:
                total_share = soup_r.select('h2.main-title')[0].text.split('(')[1].split(')')[0]
                int_share = int(total_share)
                int_page=0
                if int_share%5==0:
                    int_page=int(int_share/5)
                else:
                    int_page=int(int_share/5)+1
                for i in range(1,int_page+1):

                    share_page = '/comments?p={}&sortway=d&so=shop_default'.format(i)
                    share_url = url_base + restaurant_num + share_page
                    #print(share_url)
                    
                            
                    restaurant_share(share_url)
            
        except IndexError:
            print("[ERROR] : no page!")
            
            
#爬取單一餐廳的所有食記網址
def restaurant_share(share_url):
    
    
    res = r.get(share_url)
    res.encoding="utf-8"
    soup = bs(res.text, 'lxml')

    
    comment_list = soup.find_all('a',{'itemprop':'discussionUrl url'})
    for comment in comment_list:
        comment_url = comment.get('href')
        c_url = url_base + comment_url
#         print(c_url)
        comment_page = comment.get('href').split('/')[2]
        int_comment_page = int(comment_page)
        
        if int_comment_page%4==1:
            with open('text_1.txt', 'a',encoding='utf8') as f1:
                f1.write(c_url+'\n')
                
        elif int_comment_page%4==2:
            with open('text_2.txt', 'a',encoding='utf8') as f2:
                f2.write(c_url+'\n')
        elif int_comment_page%4==3:        
            with open('text_3.txt', 'a',encoding='utf8') as f3:
                f3.write(c_url+'\n')
        else:        
            with open('text_4.txt', 'a',encoding='utf8') as f4:
                f4.write(c_url+'\n')
                

if __name__ == '__main__':                
            
     #lock = threading.Lock()  #命名一個 Lock 物件
    q = Queue() # 開一個 Queue 物件
    t1 = threading.Thread(target=page_crawler, args=(q,)) 
                                #打開一個名字叫 t1 的線程物件
                                #這個物件會去呼叫 job1
                                #同時t1導入 q 跟 lock 做現成控制

    start = time.time()
    t1.start()  #啟動 t1 線程

    t1.join()  #在 t1線程結束前阻止程式繼續運行


      

    #確認Queue是否為空，如果不是就用 q.get() 取出值
    while not q.empty():   
        all_restaurant_list(q.get())    
        
    end = time.time() 
    time = end-start
    print(time)
        
        
               