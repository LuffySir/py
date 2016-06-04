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
path = 'E:\\dataset\\polar_movie_new\\all';
path1 = 'E:\\dataset\\polar_movie_new\\all_lda_none_afterLda';
path2 = 'E:\\dataset\\polar_movie_new\\test';
path3 = 'E:\\dataset\\polar_movie_new\\test_lda'

filelist = os.listdir(path2);

# 字典减法
def subtract(d1,d2):
    res = dict()
    for key in d1:
        if key not in d2:
            res[key] = 0.000    #########
    return res

# 字典合并
def dict_add(d1,d2):
    d = dict()
    d.update(d1)
    d.update(d2)
    return d
 
def stemmer(line):

    line_low = line.lower()
    tokens = tokenizer.tokenize(line_low)
            
    stopped_tokens = [i for i in tokens if not i in en_stop]
    stopped_tokens = [i for i in stopped_tokens if not i in string.digits]
    stopped_tokens = [i for i in stopped_tokens if not len(i)<2]
            
    stemmed_tokens = [p_stemmer.stem(i) for i in stopped_tokens]
            
    return stemmed_tokens

def stmmer_sentiword(file):
    stemmed_sentiwords = []
    with open(file,'r') as file:
        for line in file:
            stemmed_tokens = stemmer(line)        
            if not stemmed_tokens in stemmed_sentiwords:
                stemmed_sentiwords.append(stemmed_tokens)
    return stemmed_sentiwords

stemmed_sentiwords = stemmer_sentiword('E:\\dataset\\sentiment word\\all.txt')
    
# 所有文本中包含词语形成的字典    
hists_all = dict()

# 包含所有文件中的文本
texts_all = []

# 循环遍历文档列表
for i in filelist:
    absfile = os.path.join(path2,i);
    # 循环对每一个文档中的词标记
    texts = []
    with open(absfile,'r') as file:
        hist = dict()
        for line in file:
            stemmed_tokens = stemmer(line)
            
            texts.append(stemmed_tokens)    
        for word in stemmed_sentiwords:
            hist[word] = hist.get(word,0) + 1
    dictionary = corpora.Dictionary(texts)
    # print(dictionary.token2id)
    corpus = [dictionary.doc2bow(text) for text in texts]
    # print(corpus)
    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=3, id2word = dictionary, passes=20)

    absfile_w = os.path.join(path3,i)

    fin = open(absfile_w,'w')
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

#####################################################################

######################################################################        
        # 合并两个字典
        all_dict = dict_add(topic_word_dict,restword)
        
        # 对字典排序,返回的是列表
        all_list = sorted(all_dict.items(), key=lambda d:d[0])
        fre = []
        for term in all_list:
            fre.append(term[1])
        
        # 写入文件
        # （词，频率）列表
        #fin.write(str(all_list))
        #fin.write("\n")
        # 频率列表
        fin.write(str(fre))
        #fin.write("\n")
    fin.close()
print('维数',len(all_dict))
print(len(hists_all))    
