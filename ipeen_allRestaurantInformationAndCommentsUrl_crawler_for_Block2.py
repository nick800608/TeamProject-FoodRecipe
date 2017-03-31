#coding=utf-8

import requests as r
from bs4 import BeautifulSoup as bs
import json 
from queue import Queue
import threading
import re
import time
import random
import os

#-------------------------

header1 = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
          'Accept-Encoding': 'gzip, deflate, sdch',
          'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4',
          'Cache-Control': 'no-cache',
          'Connection': 'keep-alive',
          'Host': 'www.ipeen.com.tw',
          'Pragma': 'no-cache',
          'DNT': '1',
          'Upgrade-Insecure-Requests': '1',
          'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) \
          Version/9.0 Mobile/13B143 Safari/601.1'
          }

#-------------------------

pre_url_str_pattern = '(http(s)?://)(www\.ipeen.com.tw/shop/)(\d+)'

restaurant_address_googleMap_pattern = '(http:\/\/maps\.google\.com\/maps\?q=)(.+$)'

phone_pattern = '(tel:)?(\(?\d{2}\)?)?(-|\s+)?(\d{3}|\d{4})(-|\s+)?(\d{4})'

time_pattern  = '(?:[Aa][Mm]|[Pp][Mm])?((?:[01][0-9]|2[0-3]?):([0-5][0-9]))'
timeInterval_pattern = '{}~{}'.format(time_pattern,time_pattern)

replace_pattern_for_TagsAndRecommendation = '(.+)(\(\d+\))'

replace_pattern = '..'

def timeIntervalRepl(matchobj):
    return matchobj.group(1)+ '~' + matchobj.group(3)

def addressRepl(matchobj):
    return matchobj.group(2)
    
def numberRepl(matchobj):
    return matchobj.group(2)  

def tagAndRecommendationRepl(matchobj):
    return matchobj.group(1)
    
gmaps_url = 'https://maps.googleapis.com/maps/api/geocode/json'
def get_location_withoutKey(address):
    params = {'sensor': 'false', 'address': '{}'.format(address)}
    res = r.get(gmaps_url, params=params)
    results = res.json()['results']
    location = results[0]['geometry']['location']
    lat = location['lat']
    lng = location['lng']
    return lat, lng
    
def allRestaurantInformationAndCommentsUrl_crawler(pre_url_str):
    
    phoneStartTime = time.time()
    
    #print(pre_url_str)
    if re.match(pre_url_str_pattern, pre_url_str) == None:        
        print('pre_url_str is not found')
    else:    
        
        mydict = {}
        
        restaurant_id = pre_url_str.split('/')[-1].split('-')[0]
        #print(restaurant_id)
        restaurant_information_url = 'http://www.ipeen.com.tw/touch/shop.php?id={}'.format(restaurant_id)
        #print(restaurant_information_url)

        try:
            res_restaurant_information = r.get(restaurant_information_url, headers=header1)
            mydict['web_url'] = restaurant_information_url
        except HTTPError:  
            raise HTTPError('[ERROR]requests error')
            return None
        
        #print(res_restaurant_information.status_code)
        res_restaurant_information.encoding="utf-8"
        soup_restaurant_information = bs(res_restaurant_information.text, 'lxml')

        #店名
        try:
            restaurant_name = soup_restaurant_information.find('span', {'itemprop': 'name'}).text
            mydict['restaurant_name'] = restaurant_name
        except:
            print("can't find restaurant_name")
			print("move to next restaurant_page")
			return None

        #餐廳地址 與 餐廳位置 與 googleMapUrl
        try:
            google_map_url = soup_restaurant_information.find('a', {'href': re.compile('(http:\/\/maps\.google\.com\/maps\?q=)')})['href']
            #print(google_map_url)
        except:
            print("can't find google_map_url")

        #餐廳地址
        try:            
            restaurant_address = re.sub(restaurant_address_googleMap_pattern ,addressRepl ,google_map_url)
            #print(restaurant_address)
            mydict['restaurant_location'] = restaurant_address
            try:
                #餐廳位置
                restaurant_lat, restaurant_lng = get_location_withoutKey(restaurant_address)
                mydict['restaurant_lat'] = restaurant_lat
                mydict['restaurant_lng'] = restaurant_lng
                restaurant_latlng = '{}_{}'.format(restaurant_lat, restaurant_lng)
                #print(restaurant_latlng)
                mydict['restaurant_latlng'] = restaurant_latlng
            except:
                print("can't get restaurant_location")
        except:
            print("can't find restaurant_address")

        #電話
        
        try:
            phone_number = soup_restaurant_information.find('span', {'itemprop': 'telephone'}).text
            if re.match(phone_pattern, phone_number):
                #print(phone_number)
                mydict['phone_number'] = phone_number
            else:
                print("can't find phone_number")
        except:
            print("can't find span for phone_number")

        try:
            first_li_under_ul = soup_restaurant_information.find('li', {'itemprop': 'aggregateRating'})

            #綜合評分
            aggregateRating_int = int(first_li_under_ul.find('span', {'itemprop': 'ratingValue'}).text)
            if aggregateRating_int != 0:
                #print(aggregateRating_int)
                mydict['avg_rate'] = aggregateRating_int
            else:
                print('無有效綜合評分')

            #平均消費&餐廳類別
            third_li_under_ul = first_li_under_ul.find_next_sibling().find_next_sibling()
            if re.match('平均消費', third_li_under_ul.text):

                avg_consume = third_li_under_ul.text.split('：')[1]
                if ',' in avg_consume:
                    c1 = avg_consume.split(',')
                    c2 = ''.join(c1)
                    #print(c2)
                    mydict['avg_consume'] = int(c2)

                else:
                    #print(avg_consume)
                    mydict['avg_consume'] = int(avg_consume)

                category = third_li_under_ul.find_next_sibling().text
                #print(category)
                mydict['category'] = category
            else:
                #print('沒有均消')

                category = third_li_under_ul.text
                #print(category)
                mydict['category'] = category
        except:
            print("can't find li_under_ul")

        #營業時間&官方網站&推薦菜&分類標籤
        all_th_in_table = soup_restaurant_information.table.findAll('th')
        #營業時間

        open_time_list = []
        for th in all_th_in_table:
            
            if th.text=='營業時間':
                #今日時間有a標籤，代表多個營業時間
                if th.find_next_sibling().a:
                    #print('多個時間')
                    th_open_hours_list = th.find_next_sibling().findAll('th')
                    #在所有th標籤裡可以找到星期幾的標籤，然後用th的下一個平輩標籤find_next_sibling()找到當天的開店時間
                    #然後檢查時間格式是否符合標準                    
                    for th in th_open_hours_list:
                        #print(th)
                        
                        if th.text=='週一':
                            Monday = th.text
                            #print(Monday)
                            pre_opne_hours_str = th.find_next_sibling().text.strip()
                            if re.match(timeInterval_pattern, pre_opne_hours_str):
                                #print('有正確時間')                                
                                pre_opne_hours_list = pre_opne_hours_str.split()
                                opne_hours_MON = ''
                                if (len(pre_opne_hours_list) > 1):
                                    for pre_opne_hours in pre_opne_hours_list:
                                        opne_hours = re.sub(timeInterval_pattern,timeIntervalRepl , pre_opne_hours)
                                        opne_hours_MON += (opne_hours + '\t')
                                    #print(opne_hours_MON)
                                else:
                                    opne_hours_MON = pre_opne_hours_list[0]
                                    #print(opne_hours_MON)
                                open_time_list.append(opne_hours_MON)                            
                            else:
                                opne_hours_MON = None
                                
                        elif th.text=='週二':
                            Tuesday = th.text
                            #print(Tuesday)
                            pre_opne_hours_str = th.find_next_sibling().text.strip()
                            if re.match(timeInterval_pattern, pre_opne_hours_str):
                                #print('有正確時間')                                
                                pre_opne_hours_list = pre_opne_hours_str.split()
                                opne_hours_TUE = ''
                                if (len(pre_opne_hours_list) > 1):
                                    for pre_opne_hours in pre_opne_hours_list:
                                        opne_hours = re.sub(timeInterval_pattern,timeIntervalRepl , pre_opne_hours)
                                        opne_hours_TUE += (opne_hours + '\t')
                                    #print(opne_hours_TUE)
                                else:
                                    opne_hours_TUE = pre_opne_hours_list[0]
                                    #print(opne_hours_TUE)
                                open_time_list.append(opne_hours_TUE)
                            else:
                                opne_hours_TUE = None
                                
                        elif th.text=='週三':
                            Wednesday = th.text
                            #print(Wednesday)
                            pre_opne_hours_str = th.find_next_sibling().text.strip()
                            if re.match(timeInterval_pattern, pre_opne_hours_str):
                                #print('有正確時間')                                
                                pre_opne_hours_list = pre_opne_hours_str.split()
                                opne_hours_WED = ''
                                if (len(pre_opne_hours_list) > 1):
                                    for pre_opne_hours in pre_opne_hours_list:
                                        opne_hours = re.sub(timeInterval_pattern,timeIntervalRepl , pre_opne_hours)
                                        opne_hours_WED += (opne_hours + '\t')
                                    #print(opne_hours_WED)
                                else:
                                    opne_hours_WED = pre_opne_hours_list[0]
                                    #print(opne_hours_WED)
                                open_time_list.append(opne_hours_WED)
                            else:
                                opne_hours_WED = None
                                
                        elif th.text=='週四':
                            Thursday = th.text
                            #print(Thursday)
                            pre_opne_hours_str = th.find_next_sibling().text.strip()
                            if re.match(timeInterval_pattern, pre_opne_hours_str):
                                #print('有正確時間')                                
                                pre_opne_hours_list = pre_opne_hours_str.split()
                                opne_hours_THU = ''
                                if (len(pre_opne_hours_list) > 1):
                                    for pre_opne_hours in pre_opne_hours_list:
                                        opne_hours = re.sub(timeInterval_pattern,timeIntervalRepl , pre_opne_hours)
                                        opne_hours_THU += (opne_hours + '\t')
                                    #print(opne_hours_THU)
                                else:
                                    opne_hours_THU = pre_opne_hours_list[0]
                                    #print(opne_hours_THU)
                                open_time_list.append(opne_hours_THU) 
                            else:
                                opne_hours_THU = None
                                
                        elif th.text=='週五':
                            Friday = th.text
                            #print(Friday)
                            pre_opne_hours_str = th.find_next_sibling().text.strip()
                            if re.match(timeInterval_pattern, pre_opne_hours_str):
                                #print('有正確時間')                                
                                pre_opne_hours_list = pre_opne_hours_str.split()
                                opne_hours_FRI = ''
                                if (len(pre_opne_hours_list) > 1):
                                    for pre_opne_hours in pre_opne_hours_list:
                                        opne_hours = re.sub(timeInterval_pattern,timeIntervalRepl , pre_opne_hours)
                                        opne_hours_FRI += (opne_hours + '\t')
                                    #print(opne_hours_FRI)
                                else:
                                    opne_hours_FRI = pre_opne_hours_list[0]
                                    #print(opne_hours_FRI)
                                open_time_list.append(opne_hours_FRI)
                            else:
                                opne_hours_FRI = None
                                
                        elif th.text=='週六':
                            Saturday = th.text
                            #print(Saturday)
                            pre_opne_hours_SAT = th.find_next_sibling().text.strip()
                            if re.match(timeInterval_pattern, pre_opne_hours_SAT):
                                #print('有正確時間')                                
                                pre_opne_hours_list = pre_opne_hours_str.split()
                                opne_hours_SAT = ''
                                if (len(pre_opne_hours_list) > 1):
                                    for pre_opne_hours in pre_opne_hours_list:
                                        opne_hours = re.sub(timeInterval_pattern,timeIntervalRepl , pre_opne_hours)
                                        opne_hours_SAT += (opne_hours + '\t')
                                    #print(opne_hours_SAT)
                                else:
                                    opne_hours_SAT = pre_opne_hours_list[0]
                                    #print(opne_hours_SAT)
                                open_time_list.append(opne_hours_SAT)
                            else:
                                opne_hours_SAT = None

                        elif th.text=='週日':
                            Sunday = th.text
                            #print(Sunday)
                            pre_opne_hours_SAT = th.find_next_sibling().text.strip()
                            if re.match(timeInterval_pattern, pre_opne_hours_SAT):
                                #print('有正確時間')                                
                                pre_opne_hours_list = pre_opne_hours_str.split()
                                opne_hours_SUN = ''
                                if (len(pre_opne_hours_list) > 1):
                                    for pre_opne_hours in pre_opne_hours_list:
                                        opne_hours = re.sub(timeInterval_pattern,timeIntervalRepl , pre_opne_hours)
                                        opne_hours_SUN += (opne_hours + '\t')
                                    #print(opne_hours_SUN)
                                else:
                                    opne_hours_SUN = pre_opne_hours_list[0]
                                    #print(opne_hours_SUN)
                                open_time_list.append(opne_hours_SUN)
                            else:
                                opne_hours_SUN = None
                                
                        else:
                            pass
                        #print('----------')
                    #print(opne_hours_MON, opne_hours_TUE,opne_hours_WED,opne_hours_THU,opne_hours_FRI,opne_hours_SAT,opne_hours_SUN)
                    mydict['open_time'] = open_time_list
            #今日時間如果沒有a標籤，代表沒有多個營業時間或是沒有設定營業時間
                else:
                    #print('一個時間或未設定營業時間')
                    pre_open_hours = th.find_next_sibling().text
                    #print(pre_open_hours)
                    if re.match(timeInterval_pattern, pre_open_hours):
                        #print('有正確時間')
                        open_hours = re.sub(timeInterval_pattern,timeIntervalRepl , pre_open_hours)
                        #print(open_hours)
                        open_time_list.append(open_hours)
                    else:
                        #print('未設定營業時間')
                        pass
                    mydict['open_time'] = open_time_list

        #官方網站&推薦菜&分類標籤
        for th in all_th_in_table:
            if th.text=='官方網站':
                #print(th)
                if th.find_next_sibling().a:
                    #print('有官方網站超連結')            
                    officialWebsite_url = th.find_next_sibling().a['href']
                    #print(officialWebsite_url)
                # else:
                    # print('無官方網站')
                
            if th.text=='推 薦 菜':
                #print(th)
                if th.find_next_sibling().a:
                    #print('有推薦菜')
                    
                    recommendation_list = []
                    
                    a_detailsRecommend_list = th.find_next_sibling().select('a')
                    #print(a_detailsRecommend_list)
                    for a in a_detailsRecommend_list:
                        pre_recommendation = a.text
                        #print(pre_recommendation)
                        recommendation = re.sub(replace_pattern_for_TagsAndRecommendation, tagAndRecommendationRepl, pre_recommendation)
                        recommendation_list.append(recommendation)
                        
                    mydict['recommended_dish'] = recommendation_list
                # else:
                    #print('無推薦菜')
            
            if th.text=='分類標籤':
                #print(th)
                if th.find_next_sibling().a:
                    #print('有分類標籤')
                    tag_list = []
                    a_Tags_list = th.find_next_sibling().select('a')
                    #print(a_Tags_list)
                    for a in a_Tags_list:
                        pre_Tag = a.text
                        #print(pre_Tag)
                        Tag = re.sub(replace_pattern_for_TagsAndRecommendation, tagAndRecommendationRepl, pre_Tag)
                        tag_list.append(Tag)
                    mydict['tags'] = tag_list
                # else:
                    #print('無分類標籤')

        #食記分享
        #判斷是否有食記分享
        if soup_restaurant_information.find('div', {'id': 'comment'}):    
            #print('有分享')    
            #取得總共有幾篇
            pre_comment_number_str = soup_restaurant_information.find('div', {'id': 'comment'}).h3.text
            
            comment_number = int(re.sub('(會員分享文\(共)(\d+)( 篇\))',numberRepl ,pre_comment_number_str))
            #print(comment_number)

            #依照篇數，計算一共有幾頁
            if comment_number <= 5:
                int_page = 1
                #print(int_page)
            elif comment_number %5 == 0:
                int_page=int(comment_number/5)
                #print(int_page)
            else:
                int_page=int(comment_number/5)+1
                #print(int_page)
                
            all_commentUrl_list = []

            #產生分享文列表的全部頁數的url
            for i in range(1,int_page+1):
                comment_page_url = 'http://www.ipeen.com.tw/touch/cmmList.php?p={}&id={}'.format(i, restaurant_id)
                #print(comment_page_url)
                some_commentUrl_list = restaurant_share(comment_page_url)
                try:
                    for commentUrl in some_commentUrl_list:
                        all_commentUrl_list.append(commentUrl)
                except:
                    return None
            
            mydict['all_commentUrl_list'] = all_commentUrl_list            
        # else:
            #print('尚無分享')

        #餐廳菜單連結
        if soup_restaurant_information.find('a', {'href': re.compile('(\.\./touch/menu.php\?id=)')}):
            #print('有餐廳菜單')
            pre_menu_url = soup_restaurant_information.find('a', {'href': re.compile('(\.\./touch/menu.php\?id=)')})['href']
            
            menu_url = pre_menu_url.replace(replace_pattern, 'http://www.ipeen.com.tw')
            #print(menu_url)
            mydict['menu_url'] = menu_url 

            #傳給下一個function
            pass
        # else:
            #print('無餐廳菜單')
        
        #print(mydict)
        
        try:
            #json_object = json.loads(mydict)
#             print('---------')
#             print(mydict['category'])
#             print('---------')
            
            json_objects_list.append(mydict)        
#             print('---------')
#             print(json_objects_list)
        except:
            print("[ERROR]restaurant_commend can't decode to JsonType")

        phoneEndTime = time.time()
        print(phoneEndTime - phoneStartTime)
        
#-----------------------------------------------


def restaurant_share(comment_page_url):    
    try:
        res_comment_page = r.get(comment_page_url, headers=header1)
    except:
        print('can not get comment_page url')
        return None
    print(res_comment_page.status_code)
    res_comment_page.encoding="utf-8"
    soup_comment_page = bs(res_comment_page.text, 'lxml')
    
    pre_comment_url_list = soup_comment_page.findAll('ol')
    
    some_commentUrl_list = []
    
    for pre_comment_url in pre_comment_url_list:
        
        comment_dict = {}
        
        this_author = pre_comment_url.select('li')[1].text.split('：')[0]
        #print(this_author)
        comment_dict['comment_author'] = this_author
    
        this_pre_comment_url = pre_comment_url.parent['href']
        #print(this_pre_comment_url)
        comment_id = this_pre_comment_url.split('=')[-1]
        #print(comment_id)
        #產生手機板URL
#         comment_url = 'http://www.ipeen.com.tw{}'.format(this_pre_comment_url)
        #產生Web版URL
        comment_url = 'http://www.ipeen.com.tw/comment/{}'.format(comment_id) 
        #print(comment_url)     
        
        comment_title = pre_comment_url.li.text
        #print(comment_title)
        
        comment_dict['comment_url'] = comment_url
        
        some_commentUrl_list.append(comment_dict)
    
    return some_commentUrl_list

#-----------------------------------------------


class AWSTimeLimitError(Exception):
    def __init__(self,msg):
        self.message=msg
   
    def __str__(self):
        return self.message

class HTTPError(Exception):
    def __init__(self,msg):
        self.message=msg
   
    def __str__(self):
        return self.message

def getExecutionTime(startTime):
    if (time.time() - startTime < 3550):
        pass
    else:
        raise AWSTimeLimitError('Time is running out')


#-----------------------------------------------


def reduce_allRestaurantInformationAndCommentsUrl_SplitBlock_function(q,startTime):
    try:
        rf = open('all_restaurant_list_block2.txt', 'r',encoding='utf8')
        restaurant_str = rf.read()
        #print(restaurant_str)
        
    except FileNotFoundError:
        print("'[ERROR]No such file or directory: 'all_restaurant_list_block2.txt'")
        raise
        
    if (restaurant_str==''):
        print('no url!')
        rf.close()
        with open('success_all_InformationAndCommentsUrl.txt', 'w', encoding='utf8') as wsf:
            wsf.write('success')
        os.remove('all_restaurant_list_block2.txt')
        
    else:
        all_restaurant_list = restaurant_str.split('\n')
        #print(all_restaurant_list)
        for restaurants in range(len(all_restaurant_list)):
            pre_url_str = all_restaurant_list.pop()
            q.put(pre_url_str)


#-----------------------------------------------


if __name__ == '__main__':   
    
    startTime = time.time()  
    lastWriteTime = time.time()    
    json_objects_list = []
    
    q = Queue()
    t1 = threading.Thread(target=reduce_allRestaurantInformationAndCommentsUrl_SplitBlock_function, args=(q,startTime,)) 
    
    t1.start()
    t1.join()

    this_time = time.time()
    this_file = 'all_RestaurantInformationAndCommentsUrl{}.json'.format(this_time)
    f1 = open(this_file, 'w',encoding='utf8')
	

   
    try:
        while not q.empty():
            time.sleep(2)
            getExecutionTime(startTime)
			
			
            if (time.time() - lastWriteTime < 30):
                pass				
            else:
                data = json.dumps(json_objects_list, ensure_ascii=False)
                f1.write(data)
                json_objects_list = []
                print('f1 has wrote')
                lastWriteTime = time.time()

            allRestaurantInformationAndCommentsUrl_crawler(q.get())
            
        with open('success_all_restaurant_list_block2.txt', 'w', encoding='utf8') as wsf:
            wsf.write('success')
        os.remove('all_restaurant_list_block2.txt')
        
    except AWSTimeLimitError:
        with open('all_restaurant_list_block2.txt', 'w', encoding='utf8') as wf:
            while not q.empty():                    
                page = q.get()
                wf.write(page + '\n')  
    except HTTPError:
        with open('all_restaurant_list_block2.txt', 'w', encoding='utf8') as wf:
            while not q.empty():                    
                page = q.get()
                wf.write(page + '\n')
    
    #print(json_objects_list)
    
    data = json.dumps(json_objects_list, ensure_ascii=False)
    
    #print(data)
    
    f1.write(data)
    print("[INFO]crawler was finish")
    
    f1.close()
    
    endTime = time.time() 
    totalExecutionTime = str(endTime-startTime)
    print('[INFO]good')
    print('[INFO]TotalExecutionTime = ' + totalExecutionTime)