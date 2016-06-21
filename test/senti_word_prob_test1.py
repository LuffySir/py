#-*_coding:utf8-*-
from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
import gensim
import os
import string

tokenizer = RegexpTokenizer(r'\w+')

# 加停用词
en_stop = get_stop_words('en')

# 词干化
p_stemmer = PorterStemmer()

path_test = 'E:\\dataset\\polar_movie_new\\test'
path_test_lda = 'E:\\dataset\\polar_movie_new\\test_lda'

pathAll = 'E:\\dataset\\polar_movie_new\\all_del10'
pathAllLda = 'E:\\dataset\\polar_movie_new\\20\\all_lda_20t'

path_senti = 'E:\\dataset\\sentiment word\\all.txt'

# 字典减法


def subtract(d1, d2):
    res = dict()
    for key in d1:
        if key not in d2:
            res[key] = 0.000
    return res

# 字典合并


def dict_add(d1, d2):
    d = dict()
    d.update(d1)
    d.update(d2)
    return d

# 所有文本连接成字符串


def getAllStr(path):
    file_str = ''
    filelist = os.listdir(path)
    for i in filelist:
        absfile = os.path.join(path, i)
        file = open(absfile, 'r')
        for line in file:
            line_low = line.lower()
            file_str += line_low
        file.close()
    return file_str

# 获取字符串中包含的情感词（存在killing->ill的情况，后面需要注意）


def getSentiWord(path):
    sentiWord = dict()
    senti_file = open(path, 'r')
    for line_senti in senti_file:
        line_senti = line_senti.replace('\n', '')
        if line_senti in file_str:
            sentiWord[line_senti] = sentiWord.get(line_senti, 0) + 1
    senti_file.close()
    sentiWordOrder = sorted(sentiWord.items(), key=lambda d: d[0])
    return sentiWordOrder


def getSentiWordStemmer(path):
    sentiWordStemmer = dict()
    senti_file = open(path, 'r')
    for line_senti in senti_file:
        line_senti = line_senti.replace('\n', '')
        if line_senti in file_str:
            sentiWordTokens = stemmer(line_senti)
            for word in sentiWordTokens:
                sentiWordStemmer[word] = sentiWordStemmer.get(word, 0) + 1
    senti_file.close()
#    sentiWordStemmerNone = sentiWordStemmer.copy()
#    for word in sentiWordStemmer.keys():
#        if sentiWordStemmer[word] < 2:
#            sentiWordStemmerNone.pop(word)
    # print(len(sentiWordStemmer))
    return sentiWordStemmer


def stemmer(line):
    line_low = line.lower()
    tokens = tokenizer.tokenize(line_low)
    stopped_tokens = [i for i in tokens if not i in en_stop]
    stopped_tokens = [i for i in stopped_tokens if not i in string.digits]
    stopped_tokens = [i for i in stopped_tokens if not len(i) < 2]
    stemmed_tokens = [p_stemmer.stem(i) for i in stopped_tokens]

    return stemmed_tokens


def getsentiWordandtextsAll(path):
    texts = []
    with open(path, 'r') as file:
        # 该文档中包含的情感词
        hist = dict()
        for line in file:
            tokens = tokenizer.tokenize(line)
            for word in tokens:
                if word in sentiWord.keys():
                    hist[word] = hist.get(word, 0) + 1
            #【该文本中的所有词】
            texts.extend(tokens)

    return (hist, texts)


def getLdaModel(path):
    filelist = os.listdir(path)
    textsAll = []
    for i in filelist:
        moviefile = os.path.join(path, i)
        hist, texts = getsentiWordandtextsAll(moviefile)
        textsAll.append(texts)
    # print(hist.keys())

    dictionary = corpora.Dictionary(textsAll)
    corpus = [dictionary.doc2bow(text) for text in textsAll]
    ldamodel = gensim.models.ldamodel.LdaModel(
        corpus, num_topics=20, id2word=dictionary, passes=20)
    return ldamodel


def outputSentiPro(path, ldaPath):
    ldamodel = getLdaModel(path)
    filelist = os.listdir(path)
    for i in filelist:
        ldafile = os.path.join(ldaPath, i)
        moviefile = os.path.join(path, i)
        hist, texts = getsentiWordandtextsAll(moviefile)
        # 文档中没出现，但all中有的情感词
        restSentiWord = subtract(sentiWord, hist)

        fin = open(ldafile, 'w')
        sentiWordDict = dict()
        for topic in ldamodel.print_topics(num_topics=20, num_words=len(texts)):
            allDict = dict()
            topic = topic[1:]
            topic2str = str(topic).strip(string.punctuation)
            topic2list = topic2str.split('+')

            for term in topic2list:
                term2list = str(term).split('*')
                if term2list[1].replace(' ', '') in hist.keys():
                    sentiWordDict[term2list[1]] = term2list[0]
            # print(sentiWordDict)
            # 合并字典
            allDict = dict_add(sentiWordDict, restSentiWord)

            # 排序
            allDictOrder = sorted(allDict.items(), key=lambda d: d[0])
            pro = []
            for term in allDictOrder:
                pro.append(term[1])
            fin.write(str(pro))
        fin.close()

# 所有文本连接成字符串
file_str = getAllStr(pathAll)
# 获取字符串中包含的情感词（存在killing->ill的情况，后面需要注意）
sentiWord = getSentiWordStemmer(path_senti)  # 487个
outputSentiPro(pathAll, pathAllLda)
