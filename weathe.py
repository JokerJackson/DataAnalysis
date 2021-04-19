#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2020/12/9 5:44 下午
# @Author : JokerJackson
# @File : weathe.py
# @Software: PyCharm

import requests
from bs4 import BeautifulSoup

def get_weather_page_data(city='haerbin', year='202010'):

    city = city
    year = year

    url = 'http://tianqihoubao.com/aqi/'+city+'-'+year+'.html'
    headers = {
        'User-Agent': 'Mozilla / 5.0(Macintosh;IntelMacOSX10_15_7) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 87.0.4280.88Safari / 537.36'
    }
    get_page = requests.get(url, headers=headers).text
    bs = BeautifulSoup(get_page, 'lxml')
    trs = bs.find("div",{"class":'api_month_list'}).find_all("tr")
    td_list = []
    for item in trs:
        tds = item.find_all("td")
        td_list_item = []
        for td in tds:
            td_list_item.append(td.get_text().strip())
        td_list.append(td_list_item)
    for item in td_list:
        data = item[0]
        zhiliang = item[1]
        AQI = item[2]
        rote = item[3]
        PM2 = item[4]
        PM10 = item[5]
        So = item[6]
        No = item[7]
        Co = item[8]
        O3 = item[9]
        # print(data,zhiliang,AQI,rote,PM2,PM10,So,No,Co,O3)
        with open("data/"+city+"-"+year+".csv", "a+") as fp:
            fp.write(data+","+zhiliang+","+AQI+","+rote+","+PM2+","+PM10+","+So+","+No+","+Co+","+O3+'\n')