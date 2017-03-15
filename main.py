# coding:utf-8
def getWordDict(corpus):
    wordDict = {}
    wordVec = []
    with open(corpus) as f:
        for line in f.readlines():
            words = line.strip().split(' ')  # 现在得到的word是词的列表
            wordVec.append(words)
            for word in words:
                if word in wordDict:
                    wordDict[word] += 1
                else:
                    wordDict[word] = 1
    return wordDict, wordVec


def countAlign(corpus, resultFile, referenceFile, wordDict):
    alignDict = wordDict  # 这个最好把alignDict里面的值初始化为0
    for k, v in alignDict:
        v = 0

    with open(resultFile) as f1, open(corpus) as fc:
        for line1, linec in zip(f1.readlines(), fc.readlines()):
            aligns = line1.strip().split(' ')
            words = linec.strip().split(' ')
            for i in range(1, 1 + len(aligns)):
                for align in aligns:
                    if '-' + 'i' in align:  # 这里搞错了一点，因为这样只保证找到了，但并不能保证找到的是对的，因此还需要跟reference的对齐进行比较
                        alignDict[aligns[i - 1]] += 1


def main():
    wordDict, wordVec = getWordDict(
        '/Users/wangqinglong/Library/Mobile Documents/com~apple~CloudDocs/词对齐实验/比较/corpus.en')
    # print(wordDict)
    print(wordVec)


if __name__ == "__main__":
    main()
