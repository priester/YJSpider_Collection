import jieba
import xlwt
import xlwt.Worksheet
#1、 读取词典的方法
def readDictList(path):
    dict = []
    with open(path,'r') as fp:
        for line in fp.readlines():
            dict.append(line.strip())
    return dict

# 消极情感词典
negDict = readDictList('./负面情绪词.txt')

# 证明情感词典
posDict = readDictList('./正面情绪词.txt')

# 否定词典
noDict = readDictList('./否定词.txt')

#程度副词
plusDict = readDictList('./程度副词.txt')

# 停用词
stopDict = readDictList('./停用词.txt')
print(len(stopDict))

stopDict = [w for w in stopDict if w not in plusDict and w not  in noDict and w not in negDict and w not in posDict]

print(len(stopDict))

#2、分词去掉停用词
def seg_word(sentence):
    seg_list = jieba.cut(sentence)
    seg_result = [ w for w in seg_list if w not in stopDict]
    print(seg_result)
    return seg_result



#预测函数
def predict(s, negdict=negDict, posdict=posDict, nodict=noDict, plusdict=plusDict):
	p = 0
	sd = seg_word(s)
	for i in range(len(sd)):
		if sd[i] in negdict:
			if i>0 and sd[i-1] in nodict:
				p = p + 1
			elif i>0 and sd[i-1] in plusdict:
				p = p - 2
			else: p = p - 1
		elif sd[i] in posdict:
			if i>0 and sd[i-1] in nodict:
				p = p - 1
			elif i>0 and sd[i-1] in plusdict:
				p = p + 2
			elif i>0 and sd[i-1] in negdict:
				p = p - 1
			elif i<len(sd)-1 and sd[i+1] in negdict:
				p = p - 1
			else: p = p + 1
		elif sd[i] in nodict:
			p = p - 0.5
	return p

print(predict(readDictList('./clearArticle.txt')[1]))

originDict = readDictList('./clearArticle.txt')
print('originDict length ={}'.format(len(originDict)))

analysisDict = [w for w in originDict if len(w)>0]
print('analysisDict length ={}'.format(len(analysisDict)))


# 创建workbook
workBook = xlwt.Workbook()

# 创建表
workSheet = workBook.add_sheet('情感打分')

workSheet.write(0,0,label='内容')
workSheet.write(0,1,label='评分')

neg_scores = []
pos_scores = []
for article in analysisDict:
	workSheet.write(analysisDict.index(article)+1,0,label=article)
	score = predict(article)
	workSheet.write(analysisDict.index(article)+1,1,label=str(score))
	if score>0:
		pos_scores.append(score)
	else:
		neg_scores.append(score)

print('=====正面评价占比:{}'.format(len(pos_scores)/len(analysisDict)))

workBook.save('./result.xls')