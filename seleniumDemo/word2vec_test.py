# 参考文章
# https://blog.csdn.net/eastmount/article/details/50637476
# https://blog.csdn.net/zhuzuwei/article/details/79004650

from  gensim.models.word2vec import Word2Vec
from  gensim.models import word2vec
import  jieba
def readDictList(path):
    dict = []
    with open(path,'r') as fp:
        for line in fp.readlines():
            dict.append(line.strip())
    return dict

import re
def get_pureText(content):
    wordList = re.findall(r'[\u4e00-\u9fa5]+',content)
    pureContent = ''.join(wordList)
    return pureContent

def load_corpus(isSave=False):
    articls = readDictList('./pos_article.txt')
    corspus = []
    for article in articls:
        article = get_pureText(article)
        stop_words = readDictList('./停用词.txt')
        words = [w for w in jieba.cut(article) if w not in stop_words]
        if isSave:
            with open('./pos_all_words.txt','a') as fp:
                fp.write(' '.join(words) + '\r\n')
        corspus.append(words)
    return corspus






def trian_model():
    # # 1、加载语料
    text = load_corpus(isSave=False)

    # 2、创建一个空的模型对象
    model = Word2Vec(min_count=1, size=100)
    model.build_vocab(text)
    # model.train(text, total_examples=model.corpus_count, epochs=model.iter)

    #3、保存模型
    model.save('./pos_model')

def load_model(path):
    model =  Word2Vec.load(path)

    # 追加训练
    # model.train([['test']])
    return model

def caculate_W(corpus):

    model = load_model('./pos_model')

    # model.wv.syn0保存了特征向量
    # print(model.wv.syn0)

    # 打印的词语
    # print(len(model.wv.index2word))

    # print(model['火车站','主题','火车站'].shape)
    # print(model['火车站','主题'])
    print(model[corpus])
    return model[corpus]



from sklearn.cluster import KMeans,MiniBatchKMeans

import numpy as np
from scipy.spatial.distance import cdist
# 3、聚类
def cluster(W,corpus,n_clusters=2,resultPath=None):


    clf = MiniBatchKMeans(n_clusters=n_clusters,batch_size=1000,init_size=1000)
    s = clf.fit(W)

    print(clf.labels_)

    dic = {}
    for i in range(len(clf.labels_)):
        key = str(clf.labels_[i])
        if dic.get(key):
            arr = list(dic[key])
            arr.append(corpus[i])
            dic[key] = arr
        else:
            arr = []
            arr.append(corpus[i])
            dic[key] = arr



    print(dic)


    if resultPath:
        results = []
        for (key, value) in dic.items():
            results.append(value)
        results =  sorted(results, key=lambda x: len(x), reverse=True)
        print(results)
        write_result = []
        if n_clusters == 3:
            print('====聚完这次就要结束了========')
            write_results = results
        else:
            write_results = results
        for i in range(0,len(write_results)):
            result = write_results[i]
            with open(resultPath, 'a') as fp:
                fp.write(' '.join(result) + '\r\n')

                # if n_clusters == 3 and (i == len(write_results) - 1):
                #     return





    #用来评估簇的个数是否合适，距离越小说明簇分的越好，选取临界点的簇个数
    print('聚类完成============总的距离{}====kz值为{}'.format(clf.inertia_,n_clusters))

    # 肘部法则：
    #     如果问题中没有指定 的值，可以通过肘部法则这一技术来估计聚类数量。肘部法则会把不同 值的
    #     成本函数值画出来。随着 值的增大，平均畸变程度会减小；每个类包含的样本数会减少，于是样本
    #     离其重心会更近。但是，随着 值继续增大，平均畸变程度的改善效果会不断减低。 值增大过程

    #     中，畸变程度的改善效果下降幅度最大的位置对应的 值就是肘部
    # 平均畸变程度
    avage_change_value = sum(np.min(cdist(W, clf.cluster_centers_, 'euclidean'), axis=1)) / W.shape[0]
    # 递归算法
    # corpus = dic.get('0')
    # n_len = int(len(corpus)/5)
    # W = caculate_tfidf(corpus)
    # cluster(W, corpus, n_clusters=n_len,resultPath=resultPath)
    return avage_change_value


def test_cluster(W,corpus,clusterRange=range(2,11)):

    scores = []

    for i in clusterRange:
        scores.append(cluster(W, corpus, i))
    import matplotlib.pyplot as plt
    plt.plot(clusterRange,scores,'bx-')
    plt.title('用肘部法则来确定最佳的K值')
    plt.xlabel('K')
    plt.ylabel('平均畸变程度')

    plt.legend()
    plt.show()

def load_keys_words_corpus():
    corpus = []
    for line in readDictList('./pos_words.txt'):
        words = line.split(' ')
        for word in words:
            corpus.append(word)

    return corpus


if __name__ == '__main__':

    # 训练模型
    # trian_model()

    corpus = list(set(load_keys_words_corpus()))

    print('总共多少词汇{}'.format(len(corpus)))


    W = caculate_W(corpus)



    cluster(W,corpus=corpus,n_clusters=29,resultPath='./word2vec_rest.txt')
    # test_cluster(W,corpus,range(19,50))


