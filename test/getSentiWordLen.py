from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
import gensim
import os
import string

pathAll = 'E:\\dataset\\polar_movie_new\\all_del10';
path_senti = 'E:\\dataset\\sentiment word\\all.txt';

tokenizer = RegexpTokenizer(r'\w+')

# 加停用词
en_stop = get_stop_words('en')

# 词干化
p_stemmer = PorterStemmer()

def getAllStr(path):
    file_str = ''
    filelist = os.listdir(path);
    for i in filelist:
        absfile = os.path.join(path,i)
        file = open(absfile,'r')
        for line in file:
            line_low = line.lower()
            file_str += line_low
        file.close()
    return file_str

def stemmer(line):
    line_low = line.lower()
    tokens = tokenizer.tokenize(line_low)            
    stopped_tokens = [i for i in tokens if not i in en_stop]
    stopped_tokens = [i for i in stopped_tokens if not i in string.digits]
    stopped_tokens = [i for i in stopped_tokens if not len(i)<2]
    stemmed_tokens = [p_stemmer.stem(i) for i in stopped_tokens]

    return stemmed_tokens

def getSentiWordStemmer(path):
    sentiWordStemmer = dict()
    senti_file = open(path,'r')
    for line_senti in senti_file:
        line_senti = line_senti.replace('\n','')
        if line_senti in file_str:
            sentiWordTokens = stemmer(line_senti)
            for word in sentiWordTokens:
                sentiWordStemmer[word] = sentiWordStemmer.get(word,0)+1
    senti_file.close()
#    sentiWordStemmerNone = sentiWordStemmer.copy()
#    for word in sentiWordStemmer.keys():
#        if sentiWordStemmer[word] < 2:
#            sentiWordStemmerNone.pop(word)
    #print(len(sentiWordStemmer))
    return sentiWordStemmer

file_str = getAllStr(pathAll)
sentiWord = getSentiWordStemmer(path_senti)
print(len(sentiWord))
