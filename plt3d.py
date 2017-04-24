# coding:utf-8
from __future__ import division
import matplotlib.pyplot as plt


def getTestDict(testPath):  # 得到测试集中每个词的出现次数
    testDict = {}
    with open(testPath) as f:
        for line in f.readlines():
            words = line.strip().split(' ')  # 现在得到的word是词的列表
            for word in words:
                if word in testDict:
                    testDict[word] += 1
                else:
                    testDict[word] = 1
    return testDict


def getCorpusDict(corpusPath, testDict):  # 得到测试集中的词在训练集中出现的次数
    corpusDict = dict(testDict)
    for k in corpusDict:
        corpusDict[k] = 0
    with open(corpusPath) as fc:
        for line in fc.readlines():
            words = line.strip().split(' ')
            for word in words:
                if word in corpusDict:
                    corpusDict[word] += 1
    return corpusDict


def getIncreCorpusDict(corpusDict16, corpusDict26):  # 得到测试集中的词在训练集中出现的次数的变化
    increCorpusDict = {}
    for word in corpusDict26:
        increCorpusDict[word] = corpusDict26[word] - corpusDict16[word]
    return increCorpusDict


# testPath 测试集文件 resultPath 测试集对齐结果文件 referencePath 测试集对齐参考文件 testDict 测试集文件中的词典
def getAlignDict(testPath, resultPath, referencePath, testDict):  # 得到测试集中的每个词在结果文件中和参考文件中对齐一样的次数
    alignDict = dict(testDict)  # 这个最好把alignDict里面的值初始化为0
    for k in alignDict:
        alignDict[k] = 0

    with open(resultPath) as f1, open(referencePath) as f2, open(testPath) as fc:
        for line1, line2, linec in zip(f1.readlines(), f2.readlines(), fc.readlines()):
            aligns1 = line1.strip().split(' ')
            aligns2 = line2.strip().split(' ')
            words = linec.strip().split(' ')
            for i in range(1, 1 + len(aligns1)):  # 总觉得下面的计算有问题
                str_i = str(i)
                for align1 in aligns1:
                    if '-' + str_i in align1:  # 小短杠加序号在对齐结果中
                        for align2 in aligns2:
                            if align1 in align2:  # 在对齐结果中的找到的对齐在参考对齐文件中
                                alignDict[words[i - 1]] += 1
                                break  # 既然这里用了break，那么上面用in就说不过去了，
                        break  # 加入break是为了防止重复计算，但是为什么会重复我也没有想明白
    return alignDict


def getPrecRate(alignDict, testDict):  # 得到正确率，由于所有的正确的对齐个数等于测试集中的词数，因此这里可以直接比上词数
    precRateDict = dict(alignDict)
    for k in precRateDict:
        precRateDict[k] = alignDict[k] / testDict[k]

    return precRateDict


def getIncrePrecRate(precRateDict16, precRateDict26):
    increPrecRate = {}
    for word in precRateDict26:
        increPrecRate[word] = precRateDict26[word] - precRateDict16[word]

    return increPrecRate


def getChangeWord(increPrecRate):
    changeWord = []
    for word, rate in increPrecRate.items():
        if rate != 0:
            changeWord.append(word)
    return changeWord


def getReverseDict(myDict):
    reverseDict = {}
    for k, v in myDict.items():
        if v in reverseDict:
            reverseDict[v].append(k)
        else:
            reverseDict[v] = []
            reverseDict[v].append(k)
    return reverseDict


def getCluster(corpusDict16, increCorpusDict, increPrecRate):
    ddl = {}
    reverseCorpusDict16 = getReverseDict(corpusDict16)
    for cnt in reverseCorpusDict16:
        ddl[cnt] = {}
        for word in reverseCorpusDict16[cnt]:
            if increCorpusDict[word] in ddl[cnt]:
                ddl[cnt][increCorpusDict[word]].append(increPrecRate[word])
            else:
                ddl[cnt][increCorpusDict[word]] = []
                ddl[cnt][increCorpusDict[word]].append(increPrecRate[word])

    ddn = {}
    for cnt_16 in ddl:
        ddn[cnt_16] = {}
        for cnt_incre in ddl[cnt_16]:
            temp_sum = 0
            i = 0
            for prec_incre in ddl[cnt_16][cnt_incre]:
                temp_sum += prec_incre
                i += 1
            ddn[cnt_16][cnt_incre] = temp_sum / i

    ddn_not0 = {}
    for cnt_16 in ddn:
        ddn_not0[cnt_16] = {}
        for cnt_incre, prec_incre in ddn[cnt_16].items():
            if prec_incre != 0:
                ddn_not0[cnt_16][cnt_incre] = prec_incre

        if not ddn_not0[cnt_16]:
            ddn_not0.pop(cnt_16)
    return ddn, ddn_not0


def main():
    testDict = getTestDict(
        '/Users/wangqinglong/Library/Mobile Documents/com~apple~CloudDocs/WordAlign/Compare/corpus.en')
    corpusDict16 = getCorpusDict(
        '/Users/wangqinglong/Library/Mobile Documents/com~apple~CloudDocs/WordAlign/Compare/corpus.h16.en', testDict)
    corpusDict26 = getCorpusDict(
        '/Users/wangqinglong/Library/Mobile Documents/com~apple~CloudDocs/WordAlign/Compare/corpus.26.en', testDict)
    increCorpusDict = getIncreCorpusDict(corpusDict16, corpusDict26)
    alignDict16 = getAlignDict(
        '/Users/wangqinglong/Library/Mobile Documents/com~apple~CloudDocs/WordAlign/Compare/corpus.en',
        '/Users/wangqinglong/Library/Mobile Documents/com~apple~CloudDocs/WordAlign/Compare/infer.16.align',
        '/Users/wangqinglong/Library/Mobile Documents/com~apple~CloudDocs/WordAlign/Compare/test.qin.align',
        testDict)
    alignDict26 = getAlignDict(
        '/Users/wangqinglong/Library/Mobile Documents/com~apple~CloudDocs/WordAlign/Compare/corpus.en',
        '/Users/wangqinglong/Library/Mobile Documents/com~apple~CloudDocs/WordAlign/Compare/infer.26.align',
        '/Users/wangqinglong/Library/Mobile Documents/com~apple~CloudDocs/WordAlign/Compare/test.qin.align',
        testDict)
    precRateDict16 = getPrecRate(alignDict16, testDict)
    precRateDict26 = getPrecRate(alignDict26, testDict)
    increPrecRate = getIncrePrecRate(precRateDict16, precRateDict26)
    changeWord = getChangeWord(increCorpusDict)
    changeRate = getChangeWord(increPrecRate)
    # print (corpusDict16)
    # print (len(corpusDict16))
    # print (increCorpusDict)
    # print (len(increCorpusDict))
    # print (increPrecRate)
    # print (len(increPrecRate))
    # print (changeWord)
    # print (len(changeWord))
    # print (changeRate)
    # print (len(changeRate))

    ddn, ddn_not0 = getCluster(corpusDict16, increCorpusDict, increPrecRate)
    print (ddn)
    print (len(ddn))
    print (ddn_not0)
    print (len(ddn_not0))
    ddn_not0 = sorted(ddn_not0.iteritems(), key=lambda d: d[0])
    print (ddn_not0)
    print (len(ddn_not0))




    # print (reverseCorpusDict16)
    # print (len(reverseCorpusDict16))


if __name__ == "__main__":
    main()
