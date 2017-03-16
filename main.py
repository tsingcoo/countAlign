# coding:utf-8
from __future__ import division


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


def getAlignDict(corpus, resultFile, referenceFile, wordDict):  # 得到测试街中的每个词在结果对齐文件中和参考对齐文件中一样的次数
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


def main():
    wordDict = getWordDict(
        '/Users/wangql/Library/Mobile Documents/com~apple~CloudDocs/WordAlign/Compare/corpus.en')
    print(wordDict)

    alignDict = getAlignDict(
        '/Users/wangql/Library/Mobile Documents/com~apple~CloudDocs/WordAlign/Compare/corpus.en',
        '/Users/wangql/Library/Mobile Documents/com~apple~CloudDocs/WordAlign/Compare/infer.16.align',
        '/Users/wangql/Library/Mobile Documents/com~apple~CloudDocs/WordAlign/Compare/test.qin.align',
        wordDict)
    print(alignDict)

    rateDict = computeRate(alignDict, wordDict)
    print (rateDict)

    corpusDict = getCorpusDict(
        '/Users/wangql/Library/Mobile Documents/com~apple~CloudDocs/WordAlign/Compare/corpus.h16.en',
        wordDict)
    print (corpusDict)
    print (len(corpusDict))
    reverseWordDict = reverseDict(corpusDict)
    print (reverseWordDict)


if __name__ == "__main__":
    main()
