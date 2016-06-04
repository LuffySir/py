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

# 删除每个文本中只出现一次的词语
# 即hist与remv_one的交集
def del_one(d1,d2):
    one_without = dict()
    one_without.fromkeys(x for x in d1 if x in d2)
    return one_without

# 删除字典中只出现一次的词语
### (需要考虑是先删除再提取主题还是先提取再删除)#####
###（如果提取后再删除，那么可能导致每行向量的维数不一致，
##因为每个文档中都可能存在只出现一次的词，而没被删除）###
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

def invert_dict(d):
    inverse = dict()
    for key in d:
        val = d[key]
        if val not in inverse:
            inverse[val] = [key]
        else:
            inverse[val].append(key)
    return inverse
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
inverse = invert_dict(hists_all)
print(len(inverse[1]))
