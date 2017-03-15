#coding:utf-8
def readFile(resultFile, referenceFile):
    with open(resultFile) as resultF:
        for line in resultF.readlines():
            print (line.strip())
    with open(referenceFile) as referenceF:
        for line in referenceF.xreadlines():
            print (line.strip())


def main():
    readFile('/Users/wangql/Desktop/incre/比较/infer.16.align', '/Users/wangql/Desktop/incre/比较/test.qin.align')


if __name__ == "__main__":
    main()
