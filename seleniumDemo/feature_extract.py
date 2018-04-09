from gensim import  corpora,models,matutils,interfaces
import jieba
from  jieba import analyse
from gensim.interfaces import TransformedCorpus


def readDictList(path):
    dict = []
    with open(path,'r') as fp:
        for line in fp.readlines():
            dict.append(line.strip())
    return dict



# 1.首先提取从每篇游记中提取10个关键字,构建二维矩阵语料，并写入txt中

def extract_keywords(articles,savePath,key_wordNum=10,isSave=False):
    corpus = []
    print(len(articles))
    for article in articles:
        analyse.set_stop_words('./停用词.txt')
        key_list = analyse.extract_tags(article, topK=key_wordNum)
        # stop_list = readDictList('./停用词.txt')
        # key_list = [w for w in jieba.cut(article) if w not in stop_list]
        # print(key_list)
        corpus.append(key_list)
        key_words = ','.join(key_list)
        if isSave:
            with open(savePath, 'a') as fp:
                fp.write(key_words + '\r\n')
    return corpus



def test_gensim():
    # 正面词典构建
    pos_corpus = extract_keywords(readDictList('./pos_article.txt')[:10], './pos_keywords.txt', isSave=False,
                                  key_wordNum=15)
    # 负面词典构建
    neg_corpus = extract_keywords(readDictList('./neg_article.txt'), './neg_keywords.txt', isSave=False)

    # 2.构建词典
    dic = corpora.Dictionary(pos_corpus)
    print(dic)
    # 3、把词典转为向量
    vec_corpus = [dic.doc2bow(text) for text in pos_corpus]
    print(vec_corpus)
    # 4、统计tfidf
    tfidf = models.TfidfModel(vec_corpus)
    corpus_tfidf = tfidf[vec_corpus]

import re
def get_pureText(content):
    wordList = re.findall(r'[\u4e00-\u9fa5]+',content)
    pureContent = ''.join(wordList)
    return pureContent

# 1、对游记进行切词，并去除停用词
def cut_words(articlePath,isSave=False,savePath=None):
    articles = readDictList(articlePath)
    stop_words = readDictList('./停用词.txt')

    for article in articles:
        article = get_pureText(article)
        key_words = [w for w in analyse.extract_tags(article,topK=10) if w not in stop_words]
        # print(key_words)

        for word in key_words:
            with open(savePath, 'a') as fp:
                fp.write(word + '\r\n')





#2.使用sklearn计算TF-IDF
from sklearn.feature_extraction.text import  TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer

def caculate_tfidf(path,resultPath=None):
    #1.加载语聊
    corpus = readDictList(path)
    #2.将文本中词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频矩阵
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(corpus)
    # print(X[0])

    #3.计算tf-idf值
    transformer = TfidfTransformer()
    tfidf = transformer.fit_transform(X)
    #4、获取词袋中的总的词汇数为70151
    words = vectorizer.get_feature_names()

    print('总的词汇数为{}'.format(len(words)) )
    #5、tf-idf矩阵抽取出来，元素w[i][j]表示j词在i类文本中的tf-idf权重
    Weight = tfidf.toarray()
    # print('=======================')
    # print(Weight[0])

    # for w in range(len(Weight[0])):
    #     if Weight[0][w]>0:
    #         print(words[w])

    return Weight,corpus

    #6、把结果保存
    # if resultPath:
    #     result = open(resultPath,'w')
    #     for word in words:
    #         result.write(word + ' ')
    #     result.write('========================' + '\r\n')
    #     for w in Weight:
    #         for s in w:
    #             print(s)
    #             result.write(str(s))
    #     result.close()

from sklearn.cluster import KMeans,MiniBatchKMeans

import numpy as np
from scipy.spatial.distance import cdist

# 3、聚类
def cluster(W,corpus,n_clusters=2):


    # clf = KMeans(n_clusters=n_clusters)
    clf = MiniBatchKMeans(n_clusters=n_clusters,batch_size=100,init_size=1000)
    s = clf.fit(W)

    # print(s)
    # #20个中心点
    # print(clf.cluster_centers_)


    # #每个样本所属的簇
    # print(clf.labels_)

    dic = {}
    for i in range(len(clf.labels_)):
        key = clf.labels_[i]
        if dic.get(key):
            arr = list(dic[key])
            arr.append(corpus[i])
            dic[key] = arr
        else:
            arr = []
            arr.append(corpus[i])
            dic[key] = arr

    for (key ,value) in dic.items():
        with open('./pos_cluster_result.txt','a') as fp:
            fp.write('cluser{}'.format(key) + '\r\n')
            fp.write(' '.join(value) + '\r\n')

    #用来评估簇的个数是否合适，距离越小说明簇分的越好，选取临界点的簇个数
    print('聚类完成============总的距离{}====kz值为{}'.format(clf.inertia_,n_clusters

                                                    ))

    # 肘部法则：
    #     如果问题中没有指定 的值，可以通过肘部法则这一技术来估计聚类数量。肘部法则会把不同 值的
    #     成本函数值画出来。随着 值的增大，平均畸变程度会减小；每个类包含的样本数会减少，于是样本
    #     离其重心会更近。但是，随着 值继续增大，平均畸变程度的改善效果会不断减低。 值增大过程
    #     中，畸变程度的改善效果下降幅度最大的位置对应的 值就是肘部
    # 平均畸变程度
    avage_change_value = sum(np.min(cdist(W, clf.cluster_centers_, 'euclidean'), axis=1)) / W.shape[0]

    return avage_change_value



if __name__ == '__main__':
    # 1.对证明评价进行切词
    # cut_words('./pos_article.txt',isSave=True,savePath='./pos_full_words.txt')

    # # 2.计算文档的tf-idf
    W,corpus = caculate_tfidf('./pos_full_words.txt',resultPath='./pos_result.txt')
    # #
    # # # 3、聚类
    cluster(W,corpus,n_clusters=918)
    # i = 900
    # scores = []
    # while(i<=950):
    #     scores.append(cluster(W,corpus,i))
    #     i+=1
    # import matplotlib.pyplot as plt
    # plt.plot(range(900,951),scores,'bx-')
    # plt.title('用肘部法则来确定最佳的K值')
    # plt.xlabel('K')
    # plt.ylabel('平均畸变程度')
    #
    # plt.legend()
    # plt.show()
    # print(min(scores))
    # print(scores.index(min(scores)))

