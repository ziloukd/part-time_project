import pandas as pd
from functools import reduce
from collections import Counter
from pyecharts.charts import Bar,Pie
from pyecharts import options as opts
import matplotlib.pyplot as plt
import wordcloud
import jieba
# %matplotlib inline

# 导入输出图片工具
from pyecharts.render import make_snapshot
# 使用snapshot_selenium 渲染图片
from snapshot_selenium import snapshot

# 按年份进行分组
def year_group(year):
    # 判断，有两部电影的年份包含制作国家
    if len(year) > 4:
        year = year[0:4]
    year = int(year)

    if (year > 1930) and (year <= 1939):
        return '(1930, 1939]'
    elif (year > 1939) and (year <= 1948):
        return '(1939, 1948]'
    elif (year > 1948) and (year <= 1957):
        return '(1948, 1957]'
    elif (year > 1957) and (year <= 1966):
        return '(1957, 1966]'
    elif (year > 1966) and (year <= 1975):
        return '(1966, 1975]'
    elif (year > 1975) and (year <= 1984):
        return '(1975, 1984]'
    elif (year > 1984) and (year <= 1993):
        return '(1984, 1993]'
    elif (year > 1993) and (year <= 2002):
        return '(1993, 2002]'
    elif (year > 2002) and (year <= 2011):
        return '(2002, 2011]'
    elif (year > 2011) and (year <= 2019):
        return '(2011, 2019]'


# 对电影的上映年份进行分析统计
def analyze_year():
    # pandas显示所有列或所有行
    pd.set_option('display.max_rows', None)
    df['year_range'] = df['Year'].apply(year_group)
    year = df.groupby('year_range')['MovieName'].count()
    index= year.index
    values = year.values
    ts = pd.Series(values, index=index)

    # bar = Bar()
    # #x轴数据
    # bar.add_xaxis(list(index))
    # # y轴数据
    # bar.add_yaxis("各年份范围电影数量的分布",[str(i) for i in values])
    # #设置标题
    # bar.set_global_opts(title_opts=opts.TitleOpts(title="各年份范围电影数量的分布"))
    #
    # # 输出保存为图片
    # make_snapshot(snapshot, bar.render(), 'year.png')

# 对电影的制作国家进行分析统计
def analyze_country():
    #lambda表达式进行以空格分开，并返回列表
    countryList = reduce(lambda x, y: x + y, list(df['Country'].apply(lambda x: x.split(' '))))
    #进行分类统计
    countryDic = Counter(countryList)
    #将字典转为DataFrame
    country_dataframe = pd.DataFrame.from_dict(countryDic, orient='index')
    print(country_dataframe)
    country = list(country_dataframe.index)
    num = list(country_dataframe.iloc[:, 0])

    bar = Bar()
    bar.add_xaxis(country[:10])
    bar.add_yaxis("各国家电影数量Top10", num[:10])
    bar.set_global_opts(title_opts=opts.TitleOpts(title="各国家电影数量Top10"))
    bar.render("./html_files/country.html")

# 对电影不同类型进行分析统计
def analyze_type():
    # 电影类型统计
    all_type = df['Type'].str.split(' ').apply(pd.Series)
    type_text = all_type.to_string(header=False, index=False)
    all_type = all_type.apply(pd.value_counts).fillna('0')
    all_type.columns = ['type1', 'type2', 'type3', 'type4', 'type5']
    all_type['type1'] = all_type['type1'].astype(int)
    all_type['type2'] = all_type['type2'].astype(int)
    all_type['type3'] = all_type['type3'].astype(int)
    all_type['type4'] = all_type['type4'].astype(int)
    all_type['type5'] = all_type['type5'].astype(int)
    all_type['all_counts'] = all_type['type1'] + all_type['type2'] \
                             + all_type['type3'] + all_type['type4'] + all_type['type5']

    all_type = all_type.sort_values(['all_counts'], ascending=False)
    # 取电影类型前10做分析
    movie_type = pd.DataFrame({'数量': all_type['all_counts']})[:10]
    print(movie_type[:10])
    movie_type.sort_values(by='数量', ascending=False).plot(kind='bar', figsize=(13, 6))
    plt.show()


    # typeList = reduce(lambda x,y:x+y,list(df['Type'].apply(lambda x: x.split(' '))))
    # typeDic = Counter(typeList)
    #
    # k = []
    # v =[]
    # for i in typeDic:
    #     k.append(i)
    #     v.append(typeDic[i])
    #
    # pie = Pie()
    # #饼状图添加数据需要[(),()]这种格式
    # pie.add("",[z for z in zip(k, v)],center=["35%", "50%"],)
    # pie.set_global_opts(title_opts=opts.TitleOpts(title="电影类型分布"),
    #                     legend_opts=opts.LegendOpts(type_="scroll", pos_left="65%", orient="vertical")
    #                     )
    # pie.render("./html_files/type.html")

#对电影评分进行分析
def analyze_rating():

    #ascending参数是设置排序方式，默认从小到大排
    rating = df.sort_values(['Rating'],ascending=False)
    #获取评分TOP10
    r = rating[['MovieName','Rating']][:10]

    bar = Bar()
    bar.add_xaxis(list(r['MovieName']))
    bar.add_yaxis("电影评分Top10", list(r['Rating']))
    bar.set_global_opts(title_opts=opts.TitleOpts(title="电影评分Top10"))
    bar.render("./html_files/rating.html")


# 对热门短评进行文本分析，做一个词云
def comment_wordcloud():
    text = ''
    for i in df['quote'].values[:]:
        text += str(i)

    counts = {}
    words = jieba.lcut(text)
    for word in words:
        if len(word) == 1:
            continue
        counts[word] = counts.get(word, 0) + 1
    # print(counts)
    print(counts)
    wcloud = wordcloud.WordCloud(
        font_path='SimSun.ttf',
        background_color= 'white',width=1000,
        max_words= 50,
        height= 860, margin= 1
    ).fit_words(counts)
    wcloud.to_file('词云.png')

if __name__ == '__main__':

    # 读取CSV文件
    df = pd.read_csv(r'./data/movies.csv')
    # analyze_year()
    # analyze_country()
    # analyze_type()
    # analyze_rating()
    comment_wordcloud()
