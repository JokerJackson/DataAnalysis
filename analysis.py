# 全国范围内
"""
全国范围内：
1、哪些城市污染比较严重，哪些省份污染比较严重？(AQI作为判断依据)
2、污染较严重省份的主要污染物是什么？
3、污染较严重城市的主要污染物是什么？
4、全国哪个季节的污染最严重？
5、2013年-2018年全国整体空气质量如何变化
全省范围内：
1、广东省的主要污染物是什么？
2、全省哪些城市污染较严重？（AQI作为判断依据）
3、全省哪个季节的污染最严重？
4、广东省的控制质量在全国的排名？
全市范围内：
1、深圳市的主要污染物是什么？
2、深圳空气质量在全国的排名？
3、深圳哪个季节的污染最严重？
"""

# 数据理解
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from pyecharts.charts import Geo

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签

def read_data():
    df = pd.read_csv("data/aqi_data_u.csv")
    df1 = pd.read_csv("data/city.csv", encoding="gbk")
    df1.rename(columns={'city': "cityname"}, inplace=True)
    # 合并两个表格
    df = pd.merge(df, df1, on="cityname", how="inner")
    return df


# 3.3 数据清洗
"""
1、o3、primary_pollutant存在缺失值。o3使用所在城市平均值填充，primary_pollutant统计数据较混乱且与项目问题无关，删除此列；
2、AQI、pm2_5、pm10、so2、no2、co、o3目前存在0值，可理解为该部分数据缺失，可用对应城市的平均值进行填充；
3、时间数据格式需要进行转换，创建季节列；
4、创建空气质量等级列；
5、列出每个城市所属的省份；
6、创建省份空气质量排名列（以AQI为基础）；
7、创建城市空气质量排名列（以AQI为基础）
"""


def data_clear(df):
    # 1、o3、primary_pollutant存在缺失值。o3使用所在城市平均值填充，primary_pollutant统计数据较混乱且与项目问题无关，删除此列；

    for city in df.cityname.value_counts().index:
        '''
        for循环计算每个城市污染物的平均值后替换NaN值
        '''
        df.loc[(df['cityname'] == city) & (df['o3'].isnull()), 'o3'] = df[df['cityname'] == city]['o3'].mean()

    # print(df['o3'].isnull().sum())

    # 删除主要污染物列
    df.drop(['primary_pollutant'], axis=1, inplace=True)
    df.head()  # 查看调整后的表格

    # print(df.isnull().any())  # 确认表格中是否还有缺失值

    # 2、AQI、pm2_5、pm10、so2、no2、co、o3目前存在0值，可理解为该部分数据缺失，可用对应城市的平均值进行填充；
    # print(df.isnull().sum()) # 将0值替换后缺失值的数量
    cities = df.cityname.value_counts().index
    for city in cities:
        '''
        for循环计算每个城市污染物的平均值后替换NaN值
        '''
        for pollutant in ['aqi', 'pm2_5', 'pm10', 'so2', 'no2', 'co', 'o3']:
            df.loc[(df['cityname'] == city) & (df[pollutant].isnull()),
                   pollutant] = df[df['cityname'] == city][pollutant].mean()
    # print(df.isnull().sum())

    # 3.时间数据格式需要进行转换，创建季节列；
    df['time'] = pd.to_datetime(df['time'])

    # 根据月份创建季节列
    seasons = {12: 'Winter',
               1: 'Winter',
               2: 'Winter',
               3: 'Spring',
               4: 'Spring',
               5: 'Spring',
               6: 'Summer',
               7: 'Summer',
               8: 'Summer',
               9: 'Autumn',
               10: 'Autumn',
               11: 'Autumn'
               }
    df['season'] = df['time'].apply(lambda x: seasons[x.month])

    # 4.创建空气质量等级列
    bin_edges = [0, 50, 100, 150, 200, 300, 1210]  # 根据AQI的划分等级设置标签
    bin_names = ['优级', '良好', '轻度污染', '中度污染', '重度污染', '重污染']
    df['空气质量'] = pd.cut(df['aqi'], bin_edges, labels=bin_names)

    # 5.列出每个城市所属的省份；

    city_province = {'即墨': '山东省', '阿坝州': '四川省', '安康': '陕西省', '阿克苏地区': '新疆维吾尔自治区',
                     '阿里地区': '西藏区', '阿拉善盟': '内蒙古自治区', '安庆': '安徽省', '安顺': '贵州省', '鞍山': '辽宁省',
                     '克孜勒苏州': '新疆维吾尔自治区', '安阳': '河南省', '蚌埠': '安徽省', '白城': '吉林省',
                     '北海': '广西壮族自治区', '宝鸡': '陕西省', '毕节': '贵州省', '白山': '吉林省', '百色': '广西壮族自治区',
                     '保山': '云南省', '包头': '内蒙古自治区', '本溪': '辽宁省', '巴彦淖尔': '内蒙古自治区',
                     '白银': '甘肃省', '巴中': '四川省', '滨州': '山东省', '亳州': '安徽省', '昌都': '西藏区',
                     '常德': '湖南省', '赤峰': '内蒙古自治区', '昌吉州': '新疆维吾尔自治区', '五家渠': '新疆维吾尔自治区',
                     '楚雄州': '云南省', '朝阳': '辽宁省', '长治': '山西省', '潮州': '广东省', '郴州': '湖南省',
                     '池州': '安徽省', '崇左': '广西壮族自治区', '滁州': '安徽省', '丹东': '辽宁省', '德宏州': '云南省',
                     '大理州': '云南省', '大庆': '黑龙江', '大同': '山西省', '定西': '甘肃省', '大兴安岭地区': '黑龙江',
                     '德阳': '四川省', '东营': '山东省', '黔南州': '贵州省', '达州': '四川省', '德州': '山东省',
                     '鄂尔多斯': '内蒙古自治区', '恩施州': '湖北省', '鄂州': '湖北省', '防城港': '广西壮族自治区',
                     '抚顺': '辽宁省', '阜新': '辽宁省', '阜阳': '安徽省', '抚州': '江西省', '广安': '四川省',
                     '贵港': '广西壮族自治区', '桂林': '广西壮族自治区', '果洛州': '青海省', '甘南州': '甘肃省',
                     '广元': '四川省', '甘孜州': '四川省', '赣州': '江西省', '海北州': '青海省', '鹤壁': '河南省',
                     '淮北': '安徽省', '河池': '广西壮族自治区', '海东地区': '青海省', '鹤岗': '黑龙江', '黄冈': '湖北省',
                     '黑河': '黑龙江', '红河州': '云南省', '怀化': '湖南省', '呼伦贝尔': '内蒙古自治区', '葫芦岛': '辽宁省',
                     '哈密地区': '新疆维吾尔自治区', '淮南': '安徽省', '黄山': '安徽省', '黄石': '湖北省',
                     '和田地区': '新疆维吾尔自治区', '海西州': '青海省', '河源': '广东省', '衡阳': '湖南省',
                     '汉中': '陕西省', '菏泽': '山东省', '贺州': '广西壮族自治区', '吉安': '江西省', '金昌': '甘肃省',
                     '晋城': '山西省', '景德镇': '江西省', '西双版纳州': '云南省', '九江': '江西省', '吉林': '吉林省',
                     '荆门': '湖北省', '佳木斯': '黑龙江', '济宁': '山东省', '酒泉': '甘肃省', '湘西州': '湖南省',
                     '鸡西': '黑龙江', '揭阳': '广东省', '嘉峪关': '甘肃省', '焦作': '河南省', '锦州': '辽宁省',
                     '晋中': '山西省', '荆州': '湖北省', '开封': '河南省', '黔东南州': '贵州省',
                     '克拉玛依': '新疆维吾尔自治区', '喀什地区': '新疆维吾尔自治区', '六安': '安徽省',
                     '来宾': '广西壮族自治区', '聊城': '山东省', '临沧': '云南省', '娄底': '湖南省', '临汾': '山西省',
                     '漯河': '河南省', '丽江': '云南省', '吕梁': '山西省', '陇南': '甘肃省', '六盘水': '贵州省',
                     '乐山': '四川省', '凉山州': '四川省', '莱芜': '山东省', '辽阳': '辽宁省', '辽源': '吉林省',
                     '临沂': '山东省', '龙岩': '福建省', '洛阳': '河南省', '林芝': '西藏区', '柳州': '广西壮族自治区'
        , '泸州': '四川省', '马鞍山': '安徽省', '牡丹江': '黑龙江', '茂名': '广东省', '眉山': '四川省',
                     '绵阳': '四川省', '梅州': '广东省', '南充': '四川省', '宁德': '福建省', '内江': '四川省',
                     '怒江州': '云南省', '南平': '福建省', '那曲地区': '西藏区', '南阳': '河南省', '平顶山': '河南省',
                     '盘锦': '辽宁省', '平凉': '甘肃省', '莆田': '福建省', '萍乡': '江西省', '濮阳': '河南省', '攀枝花':
                         '四川省', '曲靖': '云南省', '齐齐哈尔': '黑龙江', '七台河': '黑龙江', '黔西南州': '贵州省', '清远':
                         '广东省', '庆阳': '甘肃省', '钦州': '广西壮族自治区', '泉州': '福建省', '日喀则': '西藏区', '日照':
                         '山东省', '韶关': '广东省', '绥化': '黑龙江', '石河子': '新疆维吾尔自治区', '商洛': '陕西省', '三明':
                         '福建省', '三门峡': '河南省', '山南': '西藏区', '遂宁': '四川省', '四平': '吉林省', '商丘': '河南省',
                     '上饶': '江西省', '汕头': '广东省', '汕尾': '广东省', '三亚': '海南省', '邵阳': '湖南省', '十堰':
                         '湖北省', '松原': '吉林省', '双鸭山': '黑龙江', '朔州': '山西省', '宿州': '安徽省', '随州': '湖北省',
                     '泰安': '山东省', '塔城地区': '新疆维吾尔自治区', '铜川': '陕西省', '通化': '吉林省', '铁岭': '辽宁省',
                     '通辽': '内蒙古自治区', '铜陵': '安徽省', '吐鲁番地区': '新疆维吾尔自治区', '铜仁地区': '贵州省',
                     '天水': '甘肃省', '潍坊': '山东省', '威海': '山东省', '乌海': '内蒙古自治区', '芜湖': '安徽省',
                     '乌兰察布': '内蒙古自治区', '渭南': '陕西省', '文山州': '云南省', '武威': '甘肃省', '梧州':
                         '广西壮族自治区', '兴安盟': '内蒙古自治区', '许昌': '河南省', '宣城': '安徽省', '孝感': '湖北省',
                     '迪庆州': '云南省', '锡林郭勒盟': '内蒙古自治区', '咸宁': '湖北省', '湘潭': '湖南省', '新乡':
                         '河南省', '咸阳': '陕西省', '新余': '江西省', '信阳': '河南省', '忻州': '山西省', '雅安': '四川省',
                     '延安': '陕西省', '延边州': '吉林省', '宜宾': '四川省', '宜昌': '湖北省', '宜春': '江西省', '运城':
                         '山西省', '伊春': '黑龙江', '云浮': '广东省', '阳江': '广东省', '营口': '辽宁省', '榆林': '陕西省',
                     '玉林': '广西壮族自治区', '阳泉': '山西省', '玉树州': '青海省', '烟台': '山东省', '鹰潭': '江西省',
                     '玉溪': '云南省', '益阳': '湖南省', '岳阳': '湖南省', '永州': '湖南省', '淄博': '山东省', '自贡':
                         '四川省', '湛江': '广东省', '张家界': '湖南省', '周口': '河南省', '驻马店': '河南省', '昭通': '云南省',
                     '张掖': '甘肃省', '资阳': '四川省', '遵义': '贵州省', '枣庄': '山东省', '漳州': '福建省', '株洲':
                         '湖南省', '深圳': '广东省', '福州': '福建省', '舟山': '浙江省', '青岛': '山东省', '无锡': '江苏省',
                     '湖州': '浙江省', '成都': '四川省', '石家庄': '河北省', '苏州': '新疆维吾尔自治区', '连云港': '江苏省',
                     '徐州': '江苏省', '廊坊': '河北省', '常州': '江苏省', '宿迁': '江苏省', '衡水': '河北省', '兰州':
                         '甘肃省', '邢台': '河北省', '沧州': '河北省', '哈尔滨': '黑龙江', '济南': '山东省', '昆明': '云南省',
                     '扬州': '江苏省', '杭州': '浙江省', '海口': '海南省', '南京': '江苏省', '广州': '广东省', '长沙':
                         '湖南省', '厦门': '福建省', '秦皇岛': '河北省', '张家口': '河北省', '宁波': '浙江省', '南宁':
                         '广西壮族自治区', '盐城': '江苏省', '邯郸': '河北省', '贵阳': '贵州省', '衢州': '浙江省', '承德':
                         '河北省', '南通': '江苏省', '沈阳': '辽宁省', '呼和浩特': '内蒙古自治区', '中山': '广东省', '武汉':
                         '湖北省', '合肥': '安徽省', '长春': '吉林省', '嘉兴': '浙江省', '大连': '辽宁省', '台州': '浙江省',
                     '拉萨': '西藏区', '肇庆': '广东省', '西安': '陕西省', '保定': '河北省', '江门': '广东省', '西宁':
                         '青海省', '乌鲁木齐': '新疆维吾尔自治区', '绍兴': '浙江省', '淮安': '江苏省', '温州': '浙江省', '郑州':
                         '河南省', '惠州': '广东省', '泰州': '新疆维吾尔自治区', '珠海': '广东省', '南昌': '江西省', '唐山':
                         '河北省', '金华': '浙江省', '佛山': '广东省', '东莞': '广东省', '丽水': '浙江省', '太原': '山西省',
                     '镇江': '江苏省', '阿勒泰地区': '新疆维吾尔自治区', '北京': '北京', '博州': '新疆维吾尔自治区',
                     '常熟': '江苏省', '富阳': '浙江省', '固原': '宁夏回族自治区', '海门': '江苏省', '海南州': '青海省',
                     '黄南州': '青海省', ' 即墨': '山东省', '胶南': '山东省', '句容': '江苏省', '金坛': '江苏省', '江阴':
                         '江苏省', '胶州': '山东省', '库尔勒': '新疆维吾尔自治区', '昆山': '江苏省', '临安': '浙江省',
                     '莱西': '山东省', '临夏州': '甘肃省', '溧阳': '江苏省', '莱州': '山东省', '平度': '山东省', '普洱':
                         '云南省', '蓬莱': '山东省', '荣成': '山东省', '乳山': '山东省', '寿光': '山东省', '石嘴山':
                         '宁夏回族自治区', '太仓': '江苏省', '文登': '山东省', '瓦房店': '辽宁省', '吴江': '江苏省', '吴忠':
                         '宁夏回族自治区', '襄阳': '湖北省', '伊犁哈萨克州': '新疆维吾尔自治区', '义乌': '浙江省', '宜兴':
                         '江苏省', '诸暨': '浙江省', '张家港': '江苏省', '章丘': '山东省', '中卫': '宁夏回族自治区', '招远':
                         '山东省', '天津': '天津市', '重庆': '重庆市', '银川': '甘肃省', '上海': '上海市'}
    df['省份'] = df['cityname'].map(city_province)

    # 6.创建省份空气质量排名列（以AQI平均值为基础）；

    a = df.groupby('省份').mean().aqi.sort_values().index

    b = []
    for _ in range(1, a.shape[0] + 1):
        b.append(_)

    pro_rank_dic = dict(zip(a, b))

    # 匹配省名，增加排名列
    df['所属省份空气质量排名'] = df['省份'].map(pro_rank_dic)

    # 7.创建城市空气质量排名列（以AQI为基础）。
    c = df.groupby('cityname').mean().aqi.sort_values().index

    d = []
    for _ in range(1, c.shape[0] + 1):
        d.append(_)

    city_rank_dic = dict(zip(c, d))

    # 匹配城市名，增加排名列
    df['城市空气质量全国排名'] = df['cityname'].map(city_rank_dic)
    return df


# 3.4 构建模型
def data_analysis_country(df):
    plt.figure(figsize=(25, 5))
    sns.heatmap(df.corr(), vmax=1, square=False, annot=True, linewidth=1)
    plt.yticks(rotation=0)
    plt.savefig("static/analysis/country/corr-country.jpeg")

    # 使用pyecharts模块导入地图，在地图上显示城市空气质量
    from pyecharts import options as opts

    # keys = df.groupby('cityname').aqi.mean().index
    # values = df.groupby('cityname').aqi.mean().values
    #
    # geo = Geo("全国主要城市空气质量图", "data from AQI", title_color="#fff",
    #           title_pos="left", width=800, height=600,background_color='#404a59')
    #
    # # type有scatter, effectScatter, heatmap三种模式可选，可根据自己的需求选择对应的图表模式
    # geo.add("全国城市空气质量图", keys, values, visual_range=[38.072282, 193.755892],
    #         type='effectScatter',visual_text_color="#fff", symbol_size=15,is_visualmap=True, is_roam=True)
    # geo.render(path="全国主要城市空气质量图.html")

    # 最差的10个城市
    plt.figure()
    pd.DataFrame(df.groupby('cityname').aqi.mean().sort_values().tail(10)).plot.barh(figsize=(20, 10))
    plt.xlim(125, 200)
    plt.style.use('dark_background')
    plt.title('全国空气质量最差城市')
    plt.xlabel('AQI')
    plt.ylabel('城市名')
    plt.legend('AQI')
    plt.grid(linestyle=':', color='w')
    plt.savefig("static/analysis/country/end-5-city.jpeg")

    # 最佳的10个城市
    plt.figure(figsize=(20, 10))
    pd.DataFrame(df.groupby('cityname').aqi.mean().sort_values(ascending=False).tail(10)).plot.barh(
        figsize=(20, 10))
    plt.style.use('dark_background')
    plt.title('全国空气质量十佳城市')
    plt.xlabel('AQI')
    plt.ylabel('城市名')
    plt.xlim(37, 47)
    plt.legend('AQI')
    plt.grid(linestyle=':', color='w')
    plt.savefig("static/analysis/country/top-5-city.jpeg")

    # 全国最差的10个省份
    plt.figure()
    pd.DataFrame(df.groupby('省份').aqi.mean().sort_values().tail(10)).plot.barh(figsize=(20, 10))
    plt.style.use('dark_background')
    plt.title('全国空气质量最差省份')
    plt.xlabel('AQI')
    plt.ylabel('省份')
    plt.xlim(85, 120)
    plt.legend('AQI')
    plt.grid(linestyle=':', color='w')
    plt.savefig("static/analysis/country/end-5-province.jpeg")

    # 全国最佳的10个省份
    plt.figure()
    pd.DataFrame(df.groupby('省份').aqi.mean().sort_values(ascending=False).tail(10)).plot.barh(figsize=(20, 10))
    plt.style.use('dark_background')
    plt.title('全国空气质量十佳省份')
    plt.xlabel('AQI')
    plt.ylabel('省份')
    plt.xlim(40, 75)
    plt.legend('AQI')
    plt.grid(linestyle=':', color='w')
    plt.savefig("static/analysis/country/top-5-province.jpeg")

    # 问题1.2 污染最严重省份的主要污染物
    df_top10_polluted = []
    df_top10_polluted = pd.DataFrame(df_top10_polluted)
    for _ in range(0, 10):
        '''
        提取空气质量最严重的省份信息
        '''
        temp = df[df['省份'] == df.groupby('省份').aqi.mean().sort_values().tail(10).index[_]]
        df_top10_polluted = pd.concat([df_top10_polluted, temp])

    # 这里只关注轻度污染以上时的污染物情况
    df_overpolluted = df_top10_polluted[df_top10_polluted['aqi'] >= 100][
        ['aqi', 'pm2_5', 'pm10', 'so2', 'no2', 'co', 'o3']]

    plt.figure()
    sns.regplot(x='pm2_5', y='aqi', data=df_overpolluted)
    plt.savefig("static/analysis/country/province-pm2_5-country.jpeg")
    plt.figure()
    sns.regplot(x='pm10', y='aqi', data=df_overpolluted)
    plt.savefig("static/analysis/country/province-pm10-country.jpeg")
    plt.figure()
    sns.regplot(x='so2', y='aqi', data=df_overpolluted)
    plt.savefig("static/analysis/country/province-so2-country.jpeg")
    plt.figure()
    sns.regplot(x='no2', y='aqi', data=df_overpolluted)
    plt.savefig("static/analysis/country/province-no2-country.jpeg")
    plt.figure()
    sns.regplot(x='co', y='aqi', data=df_overpolluted)
    plt.savefig("static/analysis/country/province-co-country.jpeg")
    plt.figure()
    sns.regplot(x='o3', y='aqi', data=df_overpolluted)
    plt.savefig("static/analysis/country/province-o3-country.jpeg")

    # 问题1.4：全国哪个季节的污染最严重
    plt.figure()
    pd.DataFrame(df.groupby('season').aqi.mean().sort_values()).plot.barh(figsize=(15, 10))
    plt.title('全国不同季节空气质量情况')
    plt.xlabel('AQI')
    plt.ylabel('季节')
    plt.xlim(60)
    plt.legend('AQI')
    plt.grid(linestyle=':', color='w')
    plt.savefig("static/analysis/country/season-country.jpeg")

    # 问题1.5：2013年-2018年全国整体空气质量如何变化
    plt.figure()
    f, ax = plt.subplots(figsize=(14, 10))
    sns.relplot(x='time', y='aqi', kind='line', data=df, ax=ax)
    plt.savefig("static/analysis/country/line-country.jpeg")

    # 提取年和月进一步分析整体AQI情况
    times = df['time'].shape[0]
    a = []
    for _ in range(times):
        month = df['time'][_].month
        a.append(month)
    df['month'] = a

    b = []
    for i in range(times):
        year = df['time'][i].year
        b.append(year)
    df['year'] = b

    plt.figure(figsize=(30, 10))
    sns.barplot(x='month', y='aqi', hue='year', data=df)
    plt.style.use('dark_background')
    plt.ylim(50)
    plt.title('2013年~2108年全国空气质量1~12月对比')
    plt.savefig("static/analysis/country/bar-country.jpeg")

    plt.figure()
    df.groupby('year').aqi.mean().plot.bar(figsize=(20, 10))
    plt.title('全国空气质量年变化')
    plt.xticks(rotation=0)
    plt.xlabel('年')
    plt.ylabel('AQI')
    plt.ylim(60)
    plt.legend('AQI')
    plt.grid(linestyle=':', color='w')
    plt.savefig("static/analysis/country/changes-country.jpeg")


def data_analysis_province(df):
    # 2 全省范围
    # 问题2.1：广东省的主要污染物是什么？
    df_gd = df[df['省份'] == '广东省']
    df_gd_pollutant = df_gd[df_gd['aqi'] >= 100][['aqi', 'pm2_5', 'pm10', 'so2', 'no2', 'co', 'o3']]
    sns.regplot(x='pm2_5', y='aqi', data=df_gd_pollutant)
    plt.savefig("static/analysis/province/pm2_5-province.jpeg")
    sns.regplot(x='pm10', y='aqi', data=df_gd_pollutant)
    plt.savefig("static/analysis/province/pm10-province.jpeg")
    sns.regplot(x='so2', y='aqi', data=df_gd_pollutant)
    plt.savefig("static/analysis/province/so2-province.jpeg")
    sns.regplot(x='no2', y='aqi', data=df_gd_pollutant)
    plt.savefig("static/analysis/province/no2-province.jpeg")
    sns.regplot(x='co', y='aqi', data=df_gd_pollutant)
    plt.savefig("static/analysis/province/co-province.jpeg")
    sns.regplot(x='o3', y='aqi', data=df_gd_pollutant)
    plt.savefig("static/analysis/province/o3-province.jpeg")

    # 问题2.3：全省哪个季节的污染最严重
    pd.DataFrame(df_gd.groupby('season').aqi.mean().sort_values()).plot.barh(figsize=(15, 10))
    plt.title('广东省不同季节空气质量情况')
    plt.xlabel('AQI')
    plt.ylabel('季节')
    plt.xlim(50)
    plt.legend('AQI')
    plt.grid(linestyle=':', color='w')
    plt.savefig("static/analysis/province/season-province.jpeg")

    # 问题2.4：广东省空气质量在全国的排名
    print(df_gd[['省份', '所属省份空气质量排名']])


# 全市范围
def data_analysis_city(self, df):
    # 问题3.1：深圳市的主要污染物是什么
    df_sz = df[df['cityname'] == '深圳']
    df_sz_pollutant = df_sz[df_sz['aqi'] >= 100][['aqi', 'pm2_5', 'pm10', 'so2', 'no2', 'co', 'o3']]
    sns.regplot(x='pm2_5', y='aqi', data=df_sz_pollutant)
    plt.savefig("static/analysis/city/pm2_5-city.jpeg")
    sns.regplot(x='pm10', y='aqi', data=df_sz_pollutant)
    plt.savefig("static/analysis/city/pm10-city.jpeg")
    sns.regplot(x='so2', y='aqi', data=df_sz_pollutant)
    plt.savefig("static/analysis/city/so2-province.jpeg")
    sns.regplot(x='no2', y='aqi', data=df_sz_pollutant)
    plt.savefig("static/analysis/city/no2-province.jpeg")
    sns.regplot(x='co', y='aqi', data=df_sz_pollutant)
    plt.savefig("static/analysis/city/co-province.jpeg")
    sns.regplot(x='o3', y='aqi', data=df_sz_pollutant)
    plt.savefig("static/analysis/city/o3-province.jpeg")

    plt.figure(figsize=(15, 5))
    sns.heatmap(df_sz_pollutant.corr(), vmax=1, square=False, annot=True, linewidth=1)
    plt.yticks(rotation=0)
    plt.savefig("static/analysis/city/corr-city.jpeg")

    # 问题3.2：深圳空气质量在全国的排名
    rank = df_sz[['cityname', '城市空气质量全国排名']].head(1)

    # 空气质量次数图
    df_sz.groupby('空气质量').time.count().plot.bar(figsize=(10, 5))
    plt.xticks(rotation=0)
    plt.ylabel('次数')
    plt.title('2013-2018深圳空气质量次数图')
    plt.savefig("static/analysis/city/times-city.jpeg")
    # 问题3.3：深圳哪个季节的污染最严重？
    pd.DataFrame(df_sz.groupby('season').aqi.mean().sort_values()).plot.barh(figsize=(15, 10))
    plt.figure()
    plt.title('深圳不同季节空气质量情况')
    plt.xlabel('AQI')
    plt.ylabel('季节')
    plt.xlim(40)
    plt.legend('AQI')
    plt.grid(linestyle=':', color='w')
    plt.savefig("static/analysis/city/season-city.jpeg")
