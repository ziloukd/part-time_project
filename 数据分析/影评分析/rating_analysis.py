import pandas as pd 
import jieba
import wordcloud as wc
import matplotlib.pyplot as plt
from pylab import mpl
import re
import seaborn as sns
from matplotlib import dates

mpl.rcParams['font.sans-serif'] = ['FangSong'] # 指定默认字体

def task1():
    df = read_and_parse('./data/reviews.csv')
    # 根据评价类型分组
    group = df.groupby('rating')
    # 统计不同类型的评价的数量                              
    rating_type_count = group['rating'].count()
    while True:
        print('''
        1.统计不同Rating 的数量，并进行可视化
        2.评论数随时间变化趋势''')
        user_choice = input('输入查看序号：').strip()
        if not user_choice:
            break
        if user_choice == '1':
            # 1.统计不同Rating 的数量，并进行可视化
            x_label = ['力荐', '推荐', '还行', '较差', '很差']
            plt.bar(x_label,height=[rating_type_count[i] for i in x_label])
            plt.title('评论数量分布柱状图')
            plt.show()
        elif user_choice == '2':
            # 2.
            # 2.1 将字符串格式的时间转换为datatime类型
            plt.figure(figsize=(10,5))
            df['pub_time'] = pd.to_datetime(df['pub_time'])
            # 2.2. 添加一个新的pub_date
            df['pub_date'] = df['pub_time'].dt.date
            df = df[pd.to_datetime(df['pub_date']).dt.year>2019]
            # 2.3. 根据日期分组绘图
            review_date_df = df.groupby(['pub_date']).count()
            ax = sns.lineplot(x=review_date_df.index,y=review_date_df.author,marker='o')
            # 2.4 设置显示所有时间
            ax.set(xticks=review_date_df.index)
            # 2.5 设置x轴旋转
            _ = ax.set_xticklabels(review_date_df.index,rotation=90)
            # 2.6 设置x轴格式
            ax.xaxis.set_major_formatter(dates.DateFormatter("%m-%d"))
            ax.set_xlabel("发布日期")
            ax.set_ylabel("评论数量")
            plt.show()
    
def task2():
    review_df = read_and_parse('./data/reviews.csv')
    review_df['pub_time'] = pd.to_datetime(review_df['pub_time'])
    review_df = review_df.sort_values(by = 'pub_time')
    # 电视剧人物的评分
    # 力荐：+5，推荐：+4，还行：3，较差：2，很差：1
    roles = {'房似锦':0,'徐文昌':0,'张乘乘':0,'王子健':0,'楼山关':0,'朱闪闪':0,'谢亭丰':0,'鱼化龙':0,'宫蓓蓓':0,'阚文涛':0}
    roles_count = {'房似锦':0,'徐文昌':0,'张乘乘':0,'王子健':0,'楼山关':0,'朱闪闪':0,'谢亭丰':0,'鱼化龙':0,'宫蓓蓓':0,'阚文涛':0}
    role_names = list(roles.keys())
    relations = {}
    for name in role_names:
        jieba.add_word(name)
        review_df[name] = 0
    for row in review_df.index:
        rating = review_df.loc[row,'rating']
        if rating:
            content = review_df.loc[row,"content"]
            words = list(jieba.cut(content, cut_all=False))
            names = set(role_names).intersection(set(words))
            # 根据评价加分
            for name in names:
                roles_count[name] += 1
                if rating == '力荐':
                    roles[name] += 5
                elif rating == '推荐':
                    roles[name] += 4
                elif rating == '还行':
                    roles[name] +=3
                elif rating == '较差':
                    roles[name] += 2
                elif rating == '很差':
                    roles[name] += 1
            # 统计人物同时出现的次数
            for i in role_names:
                if i in content:
                    for j in role_names:
                        if j in content and (j, i) not in relations and i != j:
                            relations[(i, j)] = relations.get((i, j), 0) + 1
        # 更新数据
        for name in role_names:
            review_df.loc[row,name] = roles.get(name)
    # 总评论数
    toal_num = review_df.shape[0]
    # 总分
    toal_score = sum(roles.values())
    # 根据评论数排名
    roles_c = sorted(roles_count, key=lambda x: roles_count.get(x), reverse=True)
    while True:
        print('''
        1.关注程度
        2.受欢迎程度
        3.受欢迎程度随着时间的变化趋势可视化
        4.角色之间的关联性''')
        user_choice = input('输入查看序号：').strip()
        if not user_choice:
            break

        if user_choice == '1':
            # 1. 计算关注度
            print('关注程度：')
            for key in roles_c:
                print(f'{key}\t{round(roles_count.get(key)/toal_num, 2) * 100}%')
        elif user_choice == '2':
            # 2.计算受欢迎度
            roles_t = sorted(roles, key=lambda x: roles.get(x), reverse=True)
            print('欢迎度')
            for key in roles_t:
                print(f'{key}\t{round(roles.get(key)/toal_score, 2) * 100}%')
        elif user_choice == '3':
            role_l = roles_c[:5] + ['pub_time']
            df = review_df.loc[:,role_l]
            df['pub_date'] = df['pub_time'].dt.date
            df = df[pd.to_datetime(df['pub_date']).dt.year == 2020]
            fate = df.set_index(['pub_date'])
            for i in role_l[:5]:
                fate[i] = round(fate[i]/toal_score, 2) * 100
            print(fate)
            fate.loc[:, role_l[:5]].plot()
            plt.ylabel('关注程度(%)')
            plt.xlabel('时间')
            plt.title('关注程度随时间变化趋势折线图')
            plt.show()
        elif user_choice == '4':
            print('角色之间的关联性')
            maxRela = max([v for k,v in relations.items()])
            # 归一化处理
            relations = {k:v/maxRela for k,v in relations.items()}
            for i, j in relations.items():
                print('-'.join(i),j)

def task3():
    df = pd.read_json('./data/reviews_anjia.json')
    # 打印前前三列
    # print(df.head(3))

    while True:
        print('''
        1.数据josn转csv保存
        2.生成词云''')
        user_choice = input('输入查看序号：').strip()
        if not user_choice:
            break

        if user_choice == '1':

            # 1.json转csv
            df.to_csv('./data/reviews_anjia.csv')
        elif user_choice == '2':

            # 1.对评论进行分词，统计与“徐文昌”和“房似锦”有关的有意义词语，并绘制词云
            # 1.1 筛选和关键词有关的评论
            content_list = []
            for content in df['content']:
                if '徐文昌' in content or '房似锦' in content:
                    content_list.append(content)

            text = '|'.join(content_list)

            # 1.2分词
            counts = {}
            # 1.2.1 添加新词
            jieba.add_word('徐文昌')
            jieba.add_word('房似锦')
            # 1.2.2 添加一些停用词
            stopwords = stopwordslist('./data/my_stop_words.txt')
            words = jieba.lcut(text)
            for word in words:
                if len(word) == 1:
                    continue
                elif word not in stopwords:
                    counts[word] = counts.get(word, 0) + 1
            # 1.3 生成词云
            wcloud = wc.WordCloud(
                font_path='./data/SimSun.ttf',
                background_color= 'white',width=1000,
                max_words= 100,
                height= 860, margin= 1
            ).fit_words(counts)
            wcloud.to_file('短评词云.png')

def stopwordslist(file_path):
    stopwords = [line.strip() for line in open(file_path, 'r', encoding='utf-8').readlines()]
    return stopwords

# 文本预处理
def read_and_parse(file_path):
    df = pd.read_csv(file_path, header=0, index_col=0, dtype=str)
    # 丢去缺省值
    df = df.dropna()
    return df

if __name__ == "__main__":
    while True:
        user_choice = input('输入任务选项(直接确认可退出当前页面):\n').strip()
        if not user_choice:
            break
        elif user_choice == '1':
            task1()
        elif user_choice == '2':
            task2()
        elif user_choice == '3':
            task3()
        else:
            print('输入有误！')