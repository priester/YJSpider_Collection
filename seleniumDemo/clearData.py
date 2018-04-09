
def loadAllText():
    articles = []
    with open('./hengshan_youji.txt') as fp:
        for line in fp.readlines():
            articles.append(line.strip())
    return articles


# print(loadAllText())


def clearAllArticle():

    headWords = '旅游攻略湖南省旅游衡山旅游攻略衡山'
    footWords = '获得积表记文章被回复本篇记共含文张帮助了名举报衡山衡山去看看不再账登录注册账登录式微博微已选择举牌选择表情他她举牌举牌举牌经验值表情弹窗弹层请输用户名确定确定举牌举牌子金币回复回复明券别爱给别你去制作返回顶意见反馈面底'
    sysblom = ''
    articles = loadAllText()
    clearArticles = []
    for article in articles:
        startIndex = article.find(':')
        newArticle = article[startIndex+1:]
        wordList = [w for w in newArticle if w not in headWords and w not in footWords]
        result = ''.join(wordList)
        clearArticles.append(result)

    # print(len(clearArticles))
    for article in set(clearArticles):
        with open('./clearArticle.txt','a') as fp:
            fp.write(article + '\r\n')



# clearAllArticle()