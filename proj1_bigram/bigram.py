'''
基于人民日报标注语料（见附件），训练一个Bigram语言模型，并预测任意给定语句的语言概率。
（中文分词可以采用Jieba, SnowNLP, PkuSeg, IK Analyzer, HanLP等）

2020.10.7
'''
import jieba

def trainBigram(text):
    '''
    处理语料库文件
    :param text: 文件名
    :return:
    '''
    wdict = {} ## count word
    with open(text, 'r', encoding='utf8') as fin:
        i = 0
        for line in fin.readlines():
            line = reformSentence(line)
            countFrequency(line, wdict)
    return wdict

def reformSentence(s):
    '''
    处理语料数据，前后分别加上<BOS>, <EOS>
    :param s: 输入的语料
    :return: 处理后的s
    '''
    slist = s.split("  ")
    ns = ""
    for i in range(len(slist)):
        m = slist[i].split("/")
        if(len(m) < 2): ##排除空字符串
            continue
        word, attr = m[0], m[1]
        if i == 0:
            ns += "BOS  "
        elif attr == "w":
            if word == "。":
                ns += "EOS  "
        else:
            ns += word
            ns += "  "
    return ns

def countFrequency(s, wdict):
    '''
    统计词频保存到wdict
    :param s: 输入的字符串
    :param wdict: 二维字典
    :return:
    '''
    wlist = s.split('  ')
    for i in range(1, len(wlist) - 1):
        if(wdict.__contains__(wlist[i]) == False): ##wi没出现过
            wdict[wlist[i]] = {} #创建字典
        if(wdict[wlist[i]].__contains__(wlist[i - 1]) == False): ## wi-1~wi没出现过
            wdict[wlist[i]][wlist[i-1]] = 1
        else:
            wdict[wlist[i]][wlist[i - 1]] += 1

def goodTuring(wdict):
    '''
    :param wdict:
    :return:
    '''
    n = [0 for i in range(1262)]
    maxv = 0
    for k in wdict.keys():
        for prek in wdict[k].keys():
            if wdict[k][prek] > maxv:
                maxv = wdict[k][prek]
            n[wdict[k][prek]] += 1
    # print(maxv)
    return n

def test(s, wdict, n, N):
    '''
    输入一串字符，输出其出现的概率
    :param s:
    :param n: n[r] 表示 出现了r次的n元语法
    :param wdict:
    :param N: total num
    :return:
    '''
    wlist = s.split('/')
    for i in range(1, len(wlist)):
        r = wdict[wlist[i]][wlist[i - 1]]
        rstar = (r + 1) * n[r + 1] / n[r]
        p = rstar / N

def smoothTest(seg_list, wdict):
    s = "/".join(seg_list)
    tlist = s.split('/')
    wlist = ['BOS'] + tlist + ['EOS']
    p = 1
    eps = 0.00001
    for i in range(1, len(wlist)):
        length = 0
        if(wdict.__contains__(wlist[i]) == False):
            p *= eps
            continue
        for j in wdict[wlist[i]]:
            length += wdict[wlist[i]][j]

        if wdict[wlist[i]].__contains__(wlist[i-1]) == False:
            p *= (1 / (length + 1))
        else:
            p *= ((wdict[wlist[i]][wlist[i-1]] + 1) / (length + 1))
    return p
# s = "19980101-01-001-001/m  迈向/v  充满/v  希望/n  的/u  新/a  世纪/n  ——/w  一九九八年/t  新年/t  讲话/n  （/w  附/v  图片/n  １/m  张/q  ）/w  "
# s1 = "19980101-01-001-002/m  中共中央/nt  总书记/n  、/w  国家/n  主席/n  江/nr  泽民/nr  "
# print(reformSentence(s))
# wdict = {}
# countFrequency(reformSentence(s), wdict)
# print(wdict)
# countFrequency(reformSentence(s1), wdict)
# print(wdict)
wdict = trainBigram("rmrb1.txt")
strlist = ["我们在社会发展中迈向充满着希望的世纪。", "得接口电打法可能许明年水的防守费可证。", "武汉大学的留学生说生活很好。"]

for str in strlist:
    print("原句：" + str)
    seg_list = jieba.cut(str, cut_all=False)
    p = smoothTest(seg_list, wdict)
    print("bigram模型计算出本句出现概率:{0}".format(p))
