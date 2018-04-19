#2.使用sklearn计算TF-IDF
from sklearn.feature_extraction.text import  TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer

def caculate_tfidf(corpus):
    #1.加载语聊
    print('corpus length:{}'.format(len(corpus)))
    #2.将文本中词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频矩阵
    vectorizer = CountVectorizer(max_df=0.5,max_features=1000)
    X = vectorizer.fit_transform(corpus)
    print(X)

    #3.计算tf-idf值
    transformer = TfidfTransformer()
    tfidf = transformer.fit_transform(X)
    #4、获取词袋中的总的词汇数为70151
    words = vectorizer.get_feature_names()

    print(words)
    print('总的词汇数为{}'.format(len(words)) )
    #5、tf-idf矩阵抽取出来，元素w[i][j]表示j词在i类文本中的tf-idf权重
    Weight = tfidf.toarray()
    print('=======================')
    print(Weight)

    # for w in range(len(Weight[0])):
    #     if Weight[0][w]>0:
    #         print(words[w])

    return Weight

if __name__ == '__main__':

    corpus = ['美男 美女 美丽 好车 垃圾',
              '车子 不要 什么 鬼的 美色']

    caculate_tfidf(corpus);