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

pathAll = 'E:\\dataset\\polar_movie_new\\all';
pathPre = 'E:\\dataset\\polar_movie_new\\all_del10';

def stemmer(line):
    line_low = line.lower()
    tokens = tokenizer.tokenize(line_low)            
    stopped_tokens = [i for i in tokens if not i in en_stop]
    stopped_tokens = [i for i in stopped_tokens if not i in string.digits]
    stopped_tokens = [i for i in stopped_tokens if not len(i)<2]
    stemmed_tokens = [p_stemmer.stem(i) for i in stopped_tokens]
    ############ 删除长度小于2的词 ##############
    stemmed_tokens = [i for i in stemmed_tokens if not len(i)<2]
    ############ 删除词频为1（还是小于某一阈值）的词 ###############
    return stemmed_tokens

def del_one(path):
    filelist = os.listdir(path)
    wordNum = dict()
    for i in filelist:
        moviefile = os.path.join(path,i)
        with open(moviefile,'r') as file:
            for line in file:
                stemmed_tokens = stemmer(line)
                for word in stemmed_tokens:
                    wordNum[word] = wordNum.get(word,0) + 1
    wordNumDict = wordNum.copy()
    for word in wordNum.keys():
        if wordNum[word] < 11:
            wordNumDict.pop(word)
    return wordNumDict

def getNew(path,prePath):
    wordNumDict = del_one(path)
    print(len(wordNumDict))
    filelist = os.listdir(path)
    for i in filelist:
        moviefile = os.path.join(path,i)
        prefile = os.path.join(prePath,i)
        fin = open(prefile,'w')
        with open(moviefile,'r') as file:
            for line in file:
                stemmed_tokens = stemmer(line)
                for word in stemmed_tokens:
                    if word in wordNumDict and len(word)>2:
                        fin.write(str(word)+' ')
                fin.write('\n')
        fin.close()
getNew(pathAll,pathPre)    
