#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2020/12/9 4:19 下午
# @Author : JokerJackson
# @File : news_spider.py
# @Software: PyCharm

import requests
from bs4 import BeautifulSoup
import json


# http://news.163.com/latest/
# http://news.163.com/special/0001220O/news_json.js?0.27319639383420324
def get_content_url():
    urls = "http://news.163.com/special/0001220O/news_json.js?0.27319639383420324"
    headers = {
        'User - Agent': 'Mozilla / 5.0(Macintosh;IntelMacOSX10_15_7) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 87.0.4280.88Safari / 537.36'
    }
    get_page = requests.get(urls, headers=headers)
    second_urls = []
    news_title = []
    if get_page.status_code == 200:
        data = get_page.text
        json_data = json.loads(data[9:-1])
        for item in json_data["news"][0]:
            second_urls.append(item['l'])
            news_title.append(item['t'])

        return second_urls, news_title
