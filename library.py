import random
import dict1


#抽
def prize_all():
    r = random.randint(0,len(dict1.ramen_list)-1)
    name = dict1.ramen_list[r]
    return name

#有分店再抽，沒有直接回傳
def branch(name):
    if(name == '隱家拉麵'):
        b = random.randint(0,3)
        list1 = ['_士林店', '_芝山店', '_赤峰店', '_公館店']
        name = name + list1[b]
    elif(name == '麵屋武藏'):
        b = random.randint(0,1)
        list1 = ['_神山', '_本店']
        name = name + list1[b]
    elif(name == '鳥人拉麵'):
        b = random.randint(0,2)
        list1 = ['_台灣總店', '_中山店', '_西門店']
        name = name + list1[b]
    elif(name == '鬼金棒'):
        b = random.randint(0,2)
        name = ['鬼金棒味噌拉麵_台北本店', '鬼金棒味噌沾麵_台北本店', '鬼金棒_松江南京']
    elif(name == '柑橘'):
        b = random.randint(0,2)
        list1 = ['_Soba', '_鴨蔥','_魚水']
        name = name + list1[b]
    elif(name == '道樂拉麵'):
        b = random.randint(0,2)
        list1 = ['道樂屋台', '道樂拉麵_大北店', '道樂商店']
        name = list1[b]
    elif(name == '博多拉麵'):
        b = random.randint(0,1)
        list1 = ['_台灣總店', '_市大店']
        name = name + list1[b]
    elif(name == '樂麵屋'):
        b = random.randint(0,3)
        list1 = ['_永康店', '_永康公園店', '_西門店', '_南港店']
        name = name + list1[b]
    elif(name == '長生塩人'):
        b = random.randint(0,3)
        list1 = ['_天母', '_辛亥', '_民生', '_北投車站']
        name = name + list1[b]
    elif(name == '山嵐拉麵'):
        b = random.randint(0,3)
        list1 = ['_大安店', '_古亭店', '_公館店', '_林森八條店']
        name = name + list1[b]
    elif(name == '一蘭'):
        b = random.randint(0,1)
        list1 = ['_台灣台北本店', '_台灣台北別館']
        name = name + list1[b]
    elif(name == '一幻拉麵'):
        name = '一幻拉麵_台北信義店'
    elif(name == '鷹流蘭丸'):
        name = '鷹流蘭丸_中山店'
    elif(name == '一風堂'):
        b = random.randint(0,4)
        list1 = ['_中山本店', '_微風北車店','_台北101店','_微風南山店','_新莊宏匯店']
        name = name + list1[b]
    else:
        name = name

    return name
        
#資訊
#網頁爬蟲

import time
import os
from datetime import datetime
from selenium import webdriver
from bs4 import BeautifulSoup
def info(url):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless") #無頭模式
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
    driver.get(url=url)
    time.sleep(0.5)
    
    html_source = driver.page_source
    time.sleep(0.5)
    

    #網頁資訊取得
    soup = BeautifulSoup(html_source, 'html.parser')

    #實施偵錯
    #test = soup.find_all(class_="t39EBf GUrTXd")[0]["aria-label"]
    #print(f"{test}")

    return_list = []
    #name, address, score, critics, time, link(url)
    return_list.append(soup.find_all("title")[0].text.strip().split(' - ')[0])
    return_list.append(soup.find_all(class_="Io6YTe fontBodyMedium")[0].text.strip())
    return_list.append(soup.find_all(class_="fontDisplayLarge")[0].text.strip())
    return_list.append(soup.find_all(class_="HHrUdb fontTitleSmall rqjGif")[0].text.strip())
    try:
        temp = soup.find_all(class_="t39EBf GUrTXd")[0]["aria-label"]
        driver.close()
    except IndexError:
        try:
            driver.find_element("xpath", '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[9]/div[4]/button').click()
        
            time.sleep(1)
        
            html_source = driver.page_source
            soup = BeautifulSoup(html_source, 'html.parser')
        
            driver.close()
            temp = soup.find_all(class_="t39EBf GUrTXd")[0]["aria-label"]
        except:
            driver.find_element("xpath", '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[9]/div[4]/button').click()
        
            time.sleep(1)
        
            html_source = driver.page_source
            soup = BeautifulSoup(html_source, 'html.parser')
        
            driver.close()
            temp = soup.find_all(class_="t39EBf GUrTXd")[0]["aria-label"]

    
    time1 = ''
    
    for i in range(len(temp.split("; "))):
                time_sub = temp.split("; ")[i]
                if '.' in temp.split("; ")[i]:
                    time_sub = temp.split("; ")[i].split('.')[0]
                #print(f"偵錯'、'{len(time_sub.split('、'))}, 偵錯','{len(time_sub.split(','))}")
                #判別中英文
                if len(time_sub.split("、")) >= 2:
                    time1 += weekday_change(time_sub.split("、")[0])
                    time1 += ' '
                elif len(time_sub.split(",")) >= 2:
                    time1 += weekday_change(time_sub.split(",")[0])

                #中文處理
                for j in range(1,len(time_sub.split("、"))):
                    if '到' in time_sub.split("、")[j]:
                        time1 += time_sub.split("、")[j].split(" 到 ")[0]
                        time1 += '-'
                        time1 += time_sub.split("、")[j].split(" 到 ")[1]
                    elif '休息' in time_sub.split("、")[j]:
                        time1 += '休息\n'
                        continue

                    #時間中間加空白，最後字元跳行
                    if j != len(time_sub.split("、"))-1:
                        time1 += ' '
                    else:
                        #整段最後則不跳行
                        if i == len(temp.split("; "))-1:
                            continue
                        time1 += '\n'

                #英文處理
                for j in range(1,len(time_sub.split(","))):
                    if 'to' in time_sub.split(",")[j]:
                        time1 += time_sub.split(",")[j].split(" to ")[0]
                        time1 += '-'
                        time1 += time_sub.split(",")[j].split(" to ")[1]
                    elif '24 hour' in time_sub.split(",")[j]:
                        time1 += ' Open 24 hours\n'
                        continue
                    #時間中間加空白，最後字元跳行
                    if j != len(time_sub.split(","))-1:
                        time1 += ' '
                    else:
                        #整段最後則不跳行
                        if i == len(temp.split("; "))-1:
                            continue
                        time1 += '\n'

    return_list.append(time1)
    return_list.append(url)
    
    return return_list
    
    
        

#將星期格式化
def weekday_change(week):
    if (week == '星期一') or (week == 'Monday'):
        return '一'
    elif (week == '星期二') or (week == 'Tuesday'):
        return '二'
    elif (week == '星期三') or (week == 'Wednesday'):
        return '三'
    elif (week == '星期四') or (week == 'Thursday'):
        return '四'
    elif (week == '星期五') or (week == 'Friday'):
        return '五'
    elif (week == '星期六') or (week == 'Saturday'):
        return '六'
    elif (week == '星期日') or (week == 'Sunday'):
        return '日'
    else:
        return week


