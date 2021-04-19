from flask import Flask, render_template, request
from news_spider import get_content_url
from weathe import get_weather_page_data
from weathe_all_year import get_page_data
from analysis import *
from io import BytesIO
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import os

app = Flask(__name__)


@app.route('/')
def index():
    urls, titles = get_content_url()
    content = zip(urls, titles)
    return render_template("index.html", results=content)


@app.route('/data', methods=['POST', 'GET'])
def data_show():
    city_dict = {
        "哈尔滨": "haerbin",
        "重庆": "chongqing",
        "上海": "shanghai"
    }
    flag = False
    if request.method == "POST":
        flag = True
        year = request.form.get("year")
        month = request.form.get("month")
        city = request.form.get("city")
        if int(month) < 10:
            month = '0' + str(month)
        year2 = str(year) + str(month)
        city_ping = city_dict[city]
        print(year2, city_ping)
        if os.path.exists("data/" + city_ping + "-" + year2 + ".csv"):
            data = pd.read_csv("data/" + city_ping + "-" + year2 + ".csv")
        else:
            get_weather_page_data(city_ping, year2)
            data = pd.read_csv("data/" + city_ping + "-" + year2 + ".csv")
        n_data = np.array(data)
        data_list = n_data.tolist()

        return render_template("data_show.html", flag=flag, results=data_list, city=city, year=year, month=month)
    else:
        return render_template("data_show.html")


@app.route("/country_analysis")
def country_analysis():
    df = read_data()
    df = data_clear(df)
    data_analysis_country(df)
    return render_template("country_analysis.html")


@app.route("/province_analysis")
def province_analysis():
    df = read_data()
    df = data_clear(df)
    data_analysis_province(df)
    return render_template("province_analysis.html")


if __name__ == '__main__':
    app.run()
