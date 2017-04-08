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
                                break
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
        increPrecRate[word] = precRateDict16[word] - precRateDict26[word]

    return increPrecRate


def main():
    testDict = getTestDict('/Users/wangql/Library/Mobile Documents/com~apple~CloudDocs/WordAlign/Compare/corpus.en')
    corpusDict16 = getCorpusDict(
        '/Users/wangql/Library/Mobile Documents/com~apple~CloudDocs/WordAlign/Compare/corpus.16.en', testDict)
    corpusDict26 = getCorpusDict(
        '/Users/wangql/Library/Mobile Documents/com~apple~CloudDocs/WordAlign/Compare/corpus.26.en', testDict)
