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

# 所有文件
path = 'E:\\dataset\\polar_movie\\all';
path1 = 'E:\\dataset\\polar_movie\\all_lda_none_afterLda';
path2 = 'E:\\dataset\\polar_movie\\test';
path3 = 'E:\\dataset\\polar_movie\\test_lda'

filelist = os.listdir(path);


# 字典减法
def subtract(d1,d2):
    res = dict()
    for key in d1:
        if key not in d2:
            res[key] = 0.000    #########
    return res

# 删除字典中只出现一次的词语
### (需要考虑是先删除再提取主题还是先提取再删除)#####
def remove_one(d):
    without_one = d.copy()
    
    for key in d.keys():
        if d[key] < 2:
            # del dict[key]############有问题
            without_one.pop(key)
    return without_one

# 字典合并
def dict_add(d1,d2):
    d = dict()
    d.update(d1)
    d.update(d2)
    return d
 
def final_tokens(line):
    ## print(line,end='')
    tokenizer = RegexpTokenizer(r'\w+')
    # “don’t” which will be read as two tokens, “don” and “t.”
    line_low = line.lower()
    tokens = tokenizer.tokenize(line_low)
    # create English stop words list
    en_stop = get_stop_words('en')
    # remove stop words  from tokens
    stopped_tokens = [i for i in tokens if not i in en_stop]
    # remove digital from tokens
    stopped_tokens = [i for i in stopped_tokens if not i in string.digits]
    # 删除长度为1的词
    stopped_tokens = [i for i in stopped_tokens if not len(i)<2]
    # Create p_stemmer of class PorterStemmer
    p_stemmer = PorterStemmer()
    # stem token
    stemmed_tokens = [p_stemmer.stem(i) for i in stopped_tokens]
    return stemmed_tokens

# 所有文本中包含词语形成的字典    
hists_all = dict()

# 循环遍历文档列表
for i in filelist:
    absfile = os.path.join(path,i);
    with open(absfile,'r') as file:
        for line in file:
            stemmed_tokens = final_tokens(line)
            for word in stemmed_tokens:
                hists_all[word] = hists_all.get(word,0) + 1

# 包含所有文件中的文本
texts_all = []

# 文件夹中的文件数
files_num = 0

# 循环遍历文档列表
for i in filelist:
    absfile = os.path.join(path,i);
    # 循环对每一个文档中的词标记
    texts = []
    with open(absfile,'r') as file:
        # 每个文本中词语构成的字典
        hist = dict()
        for line in file:
                stemmed_tokens = final_tokens(line)
                for word in stemmed_tokens:
                    hist[word] = hist.get(word,0) + 1
                # add tokens to list
                texts_all.append(stemmed_tokens)
                texts.append(stemmed_tokens)

    files_num += 1

    dictionary = corpora.Dictionary(texts)
    # print(dictionary.token2id)
    corpus = [dictionary.doc2bow(text) for text in texts]
    # print(corpus)
    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=3, id2word = dictionary, passes=20)
    # 文件名即file_num编号
    files_name = str(files_num)
    absfile_w = os.path.join(path1,files_name)
    # 该文档中没出现，但语料中有的词语
    restword = subtract(remove_one(hists_all),hist)


    # 循环遍历每个主题
    for topic in ldamodel.print_topics(num_topics=3, num_words=len(hist)):
        # 主题下所有词、频率构成的字典
        all_dict = dict()
        # 去掉每个列表中的主题标号（0,1,2……）
        topic = topic[1:]
        # 去掉头尾的逗号
        topic2str = str(topic).strip(string.punctuation)
        # 该主题下所有  概率*词语  构成的列表
        topic2list = topic2str.split('+')
        # 该主题下所有词构成的字典
        topic_word_dict = dict()
               
        for term in topic2list:
            # 将概率和词语分开，保存在列表中
            term2list = str(term).split('*')
            # 单词作字典的键，概率作值
            topic_word_dict[term2list[1]] = term2list[0]
            
        # 合并两个字典
        all_dict = dict_add(topic_word_dict,restword)
        

print(len(all_dict))
    
