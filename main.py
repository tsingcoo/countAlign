# coding:utf-8
from __future__ import division
import matplotlib.pyplot as plt
import math


def getWordDict(corpus):  # 得到测试集中每个词的出现次数
    wordDict = {}
    with open(corpus) as f:
        for line in f.readlines():
            words = line.strip().split(' ')  # 现在得到的word是词的列表
            for word in words:
                if word in wordDict:
                    wordDict[word] += 1
                else:
                    wordDict[word] = 1
    return wordDict


def getAlignDict(corpus, resultFile, referenceFile, wordDict):  # 得到测试集中的每个词在结果对齐文件中和参考对齐文件中一样的次数
    alignDict = dict(wordDict)  # 这个最好把alignDict里面的值初始化为0
    for k in alignDict:
        alignDict[k] = 0

    with open(resultFile) as f1, open(referenceFile) as f2, open(corpus) as fc:
        for line1, line2, linec in zip(f1.readlines(), f2.readlines(), fc.readlines()):
            aligns1 = line1.strip().split(' ')
            aligns2 = line2.strip().split(' ')
            words = linec.strip().split(' ')
            for i in range(1, 1 + len(aligns1)):
                str_i = str(i)
                for align1 in aligns1:
                    if '-' + str_i in align1:  # 小短杠加序号在对齐结果中
                        for align2 in aligns2:
                            if align1 in align2:  # 在对齐结果中的找到的对齐在参考对齐文件中
                                alignDict[words[i - 1]] += 1
                                break
                        break  # 加入break是为了防止重复计算，但是为什么会重复我也没有想明白

    return alignDict


def computeRate(alignDict, wordDict):
    rateDict = dict(alignDict)
    for k in rateDict:
        rateDict[k] = alignDict[k] / wordDict[k]

    return rateDict


def getCorpusDict(corpus, wordDict):  # 得到测试集中的词在训练集中出现的次数
    corpusDict = dict(wordDict)
    # print (corpusDict)
    for k in corpusDict:
        corpusDict[k] = 0
    # print (corpusDict)

    with open(corpus) as fc:
        for line in fc.readlines():
            words = line.strip().split(' ')
            for word in words:
                if word in corpusDict:
                    corpusDict[word] += 1
    return corpusDict


def reverseDict(myDict):
    reverseWordDict = {}
    for k in myDict:
        if myDict[k] in reverseWordDict:
            reverseWordDict[myDict[k]].append(k)
        else:
            reverseWordDict[myDict[k]] = []
            reverseWordDict[myDict[k]].append(k)
    return reverseWordDict


def linkCountFreq(reverseCorpusDict, rateDict):
    rateTable = {}
    for k in reverseCorpusDict:
        freq = 0
        cnt = 0
        for w in reverseCorpusDict[k]:
            freq += rateDict[w]
            cnt += 1
        rateTable[k] = freq / cnt
    return rateTable


def pltRateTable(sortedRateTable):
    x = [d[0] for d in sortedRateTable]
    # print(x)
    # print (len(x))
    y = [d[1] for d in sortedRateTable]
    # print (y)
    # print (len(y))


    x10 = []
    y10 = []
    for i in range(1000):
        x10.append(x[i])
        y10.append(y[i])

    plt.figure()
    plt.plot(x10, y10)
    plt.xlabel("word freq")
    plt.ylabel("accuracy")
    plt.title("1610W")
    plt.show()


def pltRateTable2(sortedRateTable, sortedRateTable2):
    x1 = [d[0] for d in sortedRateTable]
    y1 = [d[1] for d in sortedRateTable]
    x1_100 = []
    y1_100 = []
    for i in range(400, 500):
        x1_100.append(x1[i])
        y1_100.append(y1[i])

    x2 = [d[0] for d in sortedRateTable2]
    y2 = [d[1] for d in sortedRateTable2]
    x2_100 = []
    y2_100 = []
    for i in range(400, 500):
        x2_100.append(x2[i])
        y2_100.append(y2[i])

    plt.figure()
    plt.plot(x1_100, y1_100, "x-")
    plt.plot(x2_100, y2_100, "+-")
    plt.xlabel("word freq")
    plt.ylabel("accuracy")
    plt.show()

    dif = []
    for i in range(len(x1)):
        if abs(y2[i] - y1[i]) >= 0.5:
            dif.append(x1[i])

    # print (dif)
    print (len(dif))
    return dif


def getDifWord(dif, reverseCorpusDict):
    difReverseCorpusDict = {}
    for i in range(len(dif)):
        difReverseCorpusDict[dif[i]] = reverseCorpusDict[dif[i]]
    return difReverseCorpusDict


def pltRateTable3(sortedRateTable1, sortedRateTable2, sortedRateTable3):
    x1 = [d[0] for d in sortedRateTable1]
    y1 = [d[1] for d in sortedRateTable1]
    x1_100 = []
    y1_100 = []
    for i in range(100):
        x1_100.append(x1[i])
        y1_100.append(y1[i])

    x2 = [d[0] for d in sortedRateTable2]
    y2 = [d[1] for d in sortedRateTable2]
    x2_100 = []
    y2_100 = []
    for i in range(100):
        x2_100.append(x2[i])
        y2_100.append(y2[i])

    x3 = [d[0] for d in sortedRateTable3]
    y3 = [d[1] for d in sortedRateTable3]
    x3_100 = []
    y3_100 = []
    for i in range(100):
        x3_100.append(x3[i])
        y3_100.append(y3[i])

    plt.figure()
    plt.plot(x1_100, y1_100, label='16', color='blueviolet')
    plt.plot(x2_100, y2_100, label='26', color='red')
    plt.plot(x3_100, y3_100, label='1610', color='green')
    plt.xlabel("word freq")
    plt.ylabel("accuracy")
    plt.title("blueviolet16_red26_green1610")
    plt.show()


def main():
    wordDict = getWordDict(
        '/Users/wangql/Library/Mobile Documents/com~apple~CloudDocs/WordAlign/Compare/corpus.en')
    # print(wordDict)

    ####################################################################

    alignDict = getAlignDict(
        '/Users/wangql/Library/Mobile Documents/com~apple~CloudDocs/WordAlign/Compare/corpus.en',
        '/Users/wangql/Library/Mobile Documents/com~apple~CloudDocs/WordAlign/Compare/infer.16.align',
        '/Users/wangql/Library/Mobile Documents/com~apple~CloudDocs/WordAlign/Compare/test.qin.align',
        wordDict)
    # print(alignDict)

    rateDict = computeRate(alignDict, wordDict)
    # print(rateDict)

    corpusDict = getCorpusDict(
        '/Users/wangql/Library/Mobile Documents/com~apple~CloudDocs/WordAlign/Compare/corpus.26.en',
        wordDict)
    # print(corpusDict)
    # print(len(corpusDict))


    reverseCorpusDict = reverseDict(corpusDict)
    print (reverseCorpusDict)

    rateTable = linkCountFreq(reverseCorpusDict, rateDict)
    sortedRateTable = sorted(rateTable.items(), key=lambda d: d[0])
    # pltRateTable(sortedRateTable)

    ####################################################################

    alignDict2 = getAlignDict('/Users/wangql/Library/Mobile Documents/com~apple~CloudDocs/WordAlign/Compare/corpus.en',
                              '/Users/wangql/Library/Mobile Documents/com~apple~CloudDocs/WordAlign/Compare/infer.26.align',
                              '/Users/wangql/Library/Mobile Documents/com~apple~CloudDocs/WordAlign/Compare/test.qin.align',
                              wordDict)
    rateDict2 = computeRate(alignDict2, wordDict)
    corpusDict2 = getCorpusDict(
        '/Users/wangql/Library/Mobile Documents/com~apple~CloudDocs/WordAlign/Compare/corpus.26.en',
        wordDict)
    reverseCorpusDict2 = reverseDict(corpusDict2)
    print (reverseCorpusDict2)
    rateTable2 = linkCountFreq(reverseCorpusDict2, rateDict2)
    sortedRateTable2 = sorted(rateTable2.items(), key=lambda d: d[0])

    # 得到相差较大的几组数据，将其词频存储到list中
    dif = pltRateTable2(sortedRateTable, sortedRateTable2)

    # 把相差较大的几组数据按照list从dict中提取出来
    difReverseCorpusDict = getDifWord(dif, reverseCorpusDict)
    print (difReverseCorpusDict)

    ####################################################################

    # alignDict3 = getAlignDict('/Users/wangql/Library/Mobile Documents/com~apple~CloudDocs/WordAlign/Compare/corpus.en',
    #                           '/Users/wangql/Library/Mobile Documents/com~apple~CloudDocs/WordAlign/Compare/infer.1610.align',
    #                           '/Users/wangql/Library/Mobile Documents/com~apple~CloudDocs/WordAlign/Compare/test.qin.align',
    #                           wordDict)
    # rateDict3 = computeRate(alignDict3, wordDict)
    # corpusDict3 = getCorpusDict(
    #     '/Users/wangql/Library/Mobile Documents/com~apple~CloudDocs/WordAlign/Compare/corpus.26.en',
    #     wordDict)
    # reverseCorpusDict3 = reverseDict(corpusDict3)
    # print (reverseCorpusDict3)
    # rateTable3 = linkCountFreq(reverseCorpusDict3, rateDict3)
    # sortedRateTable3 = sorted(rateTable3.items(), key=lambda d: d[0])
    #
    # pltRateTable3(sortedRateTable, sortedRateTable2, sortedRateTable3)


if __name__ == "__main__":
    main()
