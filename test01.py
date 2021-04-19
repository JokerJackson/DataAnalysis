#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2020/12/11 1:39 下午
# @Author : JokerJackson
# @File : test01.py
# @Software: PyCharm
# 污染程度饼图
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



def read_data(city="haerbin", year="2020"):

    '''读取数据'''

    # 读取并获取索引
    columns = ["日期", "质量等级", "AQI", "当天AQI排名", "PM2.5", "PM10", "So2", "No2", "Co", "O3"]
    df = pd.read_csv("data/" + str(city) + "-" + str(year) + ".csv")
    df.columns = columns

    # 将日期转换为日期类型
    df["日期"] = pd.to_datetime(df["日期"])

    # 将日期列设置成索引 原来的索引删掉
    df.set_index("日期", drop=True, inplace=True)
    return df

def func2(data):
    AQI_min = data.AQI.min()
    AQI_max = data.AQI.max()
    print(AQI_max)
    AQI_cut = pd.cut(data.AQI, bins=(AQI_min, 50, 100, 150, 200, 300, AQI_max))
    AQI_count = AQI_cut.value_counts()
    labels = ['良(50,100]', '优(0,50]', '轻度污染(100,150]', '中度污染(150,200]', '重度污染(200,300]', '严重污染(300,1210]']
    x = [i for i in AQI_count / AQI_count.sum()]
    colors = ['#32CD32', '#FFDAB9', '#8A2BE2', '#2442aa', '#dd5555', '#FFFF00']
    explode = [0, 0.1, 0, 0, 0, 0]
    plt.pie(x=x,  # 绘图的数据
            labels=labels,  # 数据标签
            colors=colors,  # 饼图颜色
            autopct="%.1f%%",  # 设置百分比
            startangle=180,  # 设置百分比
            explode=explode,  # 设置突出显示
            radius=1  # 设置饼的半径
            )
    plt.show()

data = read_data()
func2(data)
