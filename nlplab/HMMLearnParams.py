
def get_hz_py_dic():
    py_hz_file = "pinyin2hanzi.txt"
    hz_py_dic = dict()
    py_dic = dict()
    hz_list = []
    py_list = []
    py_hz_dic = dict()
    with open(py_hz_file, 'r', encoding='utf8') as fin:
        i = -1
        j = 0
        for line in fin.readlines():
            py, hz = line.split(' ')
            hzs = hz.strip('\n').split(' ')
            if(j == 0):
                py_list.append('a')
                py_dic['a'] = len(py_list) - 1
                py_hz_dic['a'] = hzs[0]
            else:
                py_list.append(py)
                py_dic[py] = len(py_list) - 1
                py_hz_dic[py] = hzs[0]
            j += 1

            hz = hz[:-1]
            for hanzi in hz:
                if(hz_py_dic.__contains__(hanzi) == False):
                    i += 1
                    hz_py_dic[hanzi] = []
                    hz_py_dic[hanzi].append(i)
                    hz_list.append(hanzi)
                hz_py_dic[hanzi].append(py)
    hz_py_dic['阿'][1] =hz_py_dic['啊'][1] = hz_py_dic['呵'][1] = hz_py_dic['锕'][1] =  hz_py_dic['吖'][1]=  hz_py_dic['腌'][1]=  hz_py_dic['嗄'][1]='a'

    return hz_py_dic, hz_list, py_list, py_dic, py_hz_dic

def train_params():
    '''
    hmm参数训练
    :return:
    '''
    dic, hzl, pyl, pyd, pyhzdic = get_hz_py_dic()
    hz_num = len(hzl)
    pi = [0 for i in range(8000)]
    pi = count_pi(dic, pi, hzl, hz_num)

    b = [[0 for aa in range(8000)] for bb in range(8000)]
    b = count_b(hzl, dic, b, pyd, pyl)

    a = [[0 for aaa in range(8000)] for bbb in range(8000)]
    a = count_a(dic, a)
    return a, b, pi, dic, hzl, pyl, pyd, pyhzdic

def count_pi(dic, pi, hz_list, i):
    file = "lexicon.txt"
    with open(file, 'r', encoding='utf8') as fin:
        for line in fin.readlines():
            lineset = line.strip('\n').split(' ')
            hanzi = lineset[0][0]
            py = lineset[1][:-1]
            if(dic.__contains__(hanzi) == False):
                i += 1
                dic[hanzi] = []
                dic[hanzi].append(i)
                dic[hanzi].append(py)
                hz_list.append(hanzi)
            pi[dic[hanzi][0]] = 1
    return pi

def count_a(hz_dic, a):
    file = "lexicon.txt"
    count_a = [0 for i in range(8000)]
    with open(file, 'r', encoding='utf8') as fin:
        for line in fin.readlines():
            lineset = line.strip('\n').split(' ')
            Q = lineset[0]
            for q in range(len(Q) - 1):
                qi = hz_dic[Q[q]][0]
                qj = hz_dic[Q[q + 1]][0]
                a[qi][qj] += 1
                count_a[qi] += 1

    for i in range(len(a)):
        for j in range(len(a[0])):
            if(count_a[i] == 0):
                count_a[i] += 1
            a[i][j] = a[i][j] / count_a[i]
    return a

def count_b(hzlist, dic, b, pydic, pylist):
    file = "lexicon.txt"
    tmplist = [0 for i in range(8000)]
    with open(file, 'r', encoding='utf8') as fin:
        for line in fin.readlines():
            lineset = line.strip('\n').split(' ')
            hanzi = lineset[0]
            for hz in range(len(hanzi)):
                py = lineset[hz + 1][:-1]
                if(dic.__contains__(hanzi[hz]) == False):
                    hzlist.append(hanzi[hz])
                    dic[hanzi[hz]] = []
                    dic[hanzi[hz]].append(len(hzlist) - 1)
                    dic[hanzi[hz]].append(py)

                j = dic[hanzi[hz]][0] #汉字序列
                if(pydic.__contains__(py) == False):
                    pylist.append(py)
                    pydic[py] = len(pylist) - 1
                k = pydic[py]
                b[j][k] += 1
                tmplist[j] += 1

    for i in range(len(b)):
        for j in range(len(b[0])):
            b[i][j] = b[i][j] / (tmplist[i] + 1) ##smooth
    return b

def write_to_data():