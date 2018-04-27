from aip import  AipNlp
import pandas as pd
import numpy as np
from pandas import DataFrame
APP_ID = '11140414'
API_KEY = '1r7R5xb1BWEbcgmVNqnObxXk'
SECRET_KEY = 'xh58KoWYwugdHU0epBETUGPFbzQq3Ion'

# 1.创建对象
client = AipNlp(APP_ID, API_KEY, SECRET_KEY)


# 1 - 酒店
# 2 - KTV3 - 丽人
# 4 - 美食餐饮
# 5 - 旅游
# 6 - 健康
# 7 - 教育
# 8 - 商业
# 9 - 房产
# 10 - 汽车
# 11 - 生活
# 12 - 购物
# 13 - 3C
def comment_tag(comment,type):
    # 2.评论观点抽取
    data = client.commentTag(comment,options={'type': type})
    return data

# 评论的情感结果
def comment_sentiment(comment):
    result = client.sentimentClassify(comment)
    print(result)
    return result

def read_neg_data():
    neg_excel = pd.read_excel('./neg.xls')
    cloums_key = '做为一本声名在外的流行书，说的还是广州的外企，按道理应该和我的生存环境差不多啊。但是一看之下，才发现相去甚远。这也就算了，还发现其中的很多规则有很强的企业个性，也就说，只是个例，而不是行例。给我们这些老油条看看也就算了，如果给那些对外企向往，或者想了解的freshman来看，实在是容易误导他们。'
    # 第一参数为行数，第一个参数为第一列
    result = neg_excel.iloc[:,0]
    # print(result.values)
    return result.values


def test():
    df = pd.DataFrame(np.random.randn(8, 4),
                      index=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'], columns=['A', 'B', 'C', 'D'])
    print(df)
    # 获取指定的行列，第一个参数为行的范围，第二参数的范围为列的范围

    print(df.loc[:, 'A'])
    print(df.loc[:, ['A', 'C']].values)

def test_sentiment(data):

    # 统计负面结果
    neg_resutls = []

    # sentiment 为0 则为负面，1，为中性，2位正面
    for text in data[:20]:
        result = comment_sentiment(text)
        sentiment_score = result['items'][0]['sentiment']
        if sentiment_score == 0:
            neg_resutls.append(sentiment_score)

    #计算正确率
    print(len(neg_resutls))
    accuracy = len(neg_resutls)/20
    print(accuracy)





if __name__ == '__main__':

    # 1.加载负面评论的数据
    neg_data = read_neg_data()
    # 2.调用结果
    test_sentiment(neg_data)

