#!/usr/bin/env python3


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from selenium import webdriver
import requests
import time, re
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import Select


content = input("請輸入想要查訊的股票型號:")
number = int(content)

# Open Webdriver
driver = webdriver.Chrome('../Stock/chromedriver')
driver.get("https://www.tdcc.com.tw/smWeb/QryStock.jsp")




def find_stock_date(number):
    stock_dates = []
    count = 0
    stock_number = str(number)
    
    ########### Find stock dates ###########
    #######################################
    # Find stock No.
    driver.find_element_by_id("StockNo").send_keys(stock_number)
    
    # Find data dates
    select = Select(driver.find_element_by_id("scaDates"))
    for op in select.options:
        stock_dates.append(op.text)
        count = count + 1 
        if count > 6:
            break
    driver.find_element_by_id("scaDates").send_keys(20190927)
    driver.find_element_by_name("sub").click()
    
    return stock_dates
    
def find_stock_data(number,stock_dates):
    stock_number = str(number)

    ########### Find stock data ###########
    ####################################### 
    time.sleep(0.2)
    driver.find_element_by_id("StockNo").send_keys(stock_number)
    time.sleep(0.2)
    driver.find_element_by_id("scaDates").send_keys(stock_dates)
    driver.find_element_by_name("sub").click()
    
    soup =  BeautifulSoup(driver.page_source)

    trs = soup.find_all('tr')
    ulist = []
    for tr in trs:
        ui = []
        for td in tr:
            ui.append(td.string)
        ulist.append(ui)
    data = pd.DataFrame(ulist)

    return data

def calculate_data(data):
    people_less1 = int(data[5].loc[11].replace(',',''))
    people_less2 = int(data[5].loc[12].replace(',',''))
    people_less3 = int(data[5].loc[13].replace(',',''))
    people_all = data[5].loc[26].replace(',','')
    people_less4 = int(people_less1) + int(people_less2)
    people_less = int(people_less1) + int(people_less2) + int(people_less3)
    people_more = int(people_all) - people_less

    volume_less1 = int(data[7].loc[11].replace(',',''))
    volume_less2 = int(data[7].loc[12].replace(',',''))
    volume_less3 = int(data[7].loc[13].replace(',',''))
    volume_less4 = int(volume_less1) + int(volume_less2)
    volume_all = int(data[7].loc[26].replace(',',''))
    volume_less = int(volume_less1) + int(volume_less2) + int(volume_less3)
    volume_more = int(volume_all) - volume_less

    #volume_per_less1 = data[9].loc[11].replace(',','')
    #volume_per_less2 = data[9].loc[12].replace(',','')
    #volume_per_less3 = data[9].loc[13].replace(',','')
    #volume_per_all = data[9].loc[26].replace(',','')
    #volume_per_less = float(volume_per_less1) + float(volume_per_less2) + float(volume_per_less3)
    #olume_per_more = float(volume_per_all) - volume_per_less

    #people = [people_less1,people_less2,people_less3,people_less,people_more,people_all]
    #volume = [volume_less1,volume_less2,volume_less3,volume_less,volume_more,volume_all]
    #volume_per = [volume_per_less1,volume_per_less2,volume_per_less3,volume_per_less,volume_per_more,volume_per_all]
    
    #people = [people_less,people_more,people_all]
    #volume = [volume_less,volume_more,volume_all]
    #volume_per = [volume_per_less,volume_per_more,volume_per_all]    
    #result = [people_less,people_more,people_all,volume_less,volume_more,volume_all,volume_per_less,volume_per_more]
    result_simple1 = [people_less1,people_less2,people_less3,people_less4]
    result_volume = [volume_less1,volume_less2,volume_less3,volume_less4]
    result_rich = [people_more,volume_more]

    return result_simple1,result_volume,result_rich


stock_dates = find_stock_date(number)
#axis_y1 = ['散戶人數','大戶人數','總人數','散戶持有股','大戶持有股','總持有股','散戶持有比例','大戶持有比例']

axis_y2 = ['less than 1 ','1-5','5-10']
p1 = []
p2 = []
p3 = []
p4 = []
v1 = []
v2 = []
v3 = []
v4 = []
r1 = []
r2 = []
date = []
#results1 = pd.DataFrame(axis_y1)

for i in stock_dates:

    data = find_stock_data(number,i)
    result_simple1,result_volume,result_rich = calculate_data(data)
    #results1[i] = pd.DataFrame(result)
    
    # people of retail
    p1.append(result_simple1[0])
    p2.append(result_simple1[1])
    p3.append(result_simple1[2])
    p4.append(result_simple1[3])


    # volume of retail
    v1.append(result_volume[0])
    v2.append(result_volume[1])
    v3.append(result_volume[2])
    v4.append(result_volume[3])    
    
    # people of rich
    r1.append(result_rich[0])
    # volume of rich
    r2.append(result_rich[1])

    date.append(i) 
    #print('calculating......')
    
driver.close()


p1.reverse()
p2.reverse()
p3.reverse()
p4.reverse()
v1.reverse()
v2.reverse()
v3.reverse()
v4.reverse()

date.reverse()
## show people of stock components
x = range(len(date))
rects1 = plt.bar(x, height=p1, width=0.5, color='red', label=axis_y2[0])
rects2 = plt.bar(x, height=p2, width=0.5, color='green', label=axis_y2[1],bottom=p1)
rects3 = plt.bar(x, height=p3, width=0.5, color='blue', label=axis_y2[2],bottom=p4)
plt.ylabel("People")
plt.xticks(x, date)
plt.xlabel("DATE")
plt.title(' Retail player of No. ' + str(number))
plt.legend(loc=[1,0])
plt.show()


## show volume of stock components
x = range(len(date))
rects1 = plt.bar(x, height=v1, width=0.5, color='red', label=axis_y2[0])
rects2 = plt.bar(x, height=v2, width=0.5, color='green', label=axis_y2[1],bottom=v1)
rects3 = plt.bar(x, height=v3, width=0.5, color='blue', label=axis_y2[2],bottom=v4)
plt.ylabel("Volume")
plt.xticks(x, date)
plt.xlabel("DATE")
plt.title(' Retail volume of No. ' + str(number))
plt.legend(loc=[1,0])
plt.show()


## show rich_people of stock components
x = range(len(date))
rects1 = plt.bar(x, height=r1, width=0.5, color='red', label="More than 10")
plt.ylabel("People")
plt.xticks(x, date)
plt.xlabel("DATE")
plt.title(' Rich people of No. ' + str(number))
plt.legend(loc=[1,0])
plt.show()

## show rich_volume of stock components
x = range(len(date))
rects1 = plt.bar(x, height=r2, width=0.5, color='red', label="More than 10")
plt.ylabel("Volume")
plt.xticks(x, date)
plt.xlabel("DATE")
plt.title(' Rich volume of No. ' + str(number))
plt.legend(loc=[1,0])
plt.show()