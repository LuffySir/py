from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
import gensim
import os

path = 'E:\\dataset\\polar_movie\\test';
list_file = os.listdir(path)

en_stop = get_stop_words('en')

# 所有文档
texts_all = []

for files in list_file:

    # 每个文件的绝对路径
    absfile = os.path.join(path,files);
    texts = []
    with open(absfile,'r') as file:
        for line in file:
            tokenizer = RegexpTokenizer(r'\w+')
            line_low = line.lower()
            tokens = tokenizer.tokenize(line_low)
            stopped_tokens = [i for i in tokens if not i in en_stop]
            p_stemmer = PorterStemmer()
            # stem token
            stemmed_tokens = [p_stemmer.stem(i) for i in stopped_tokens]
            # add tokens to list
            texts_all.append(stemmed_tokens)
            texts.append(stemmed_tokens)

# 为文档中的所有词赋予一个不同的ID
dictionary = corpora.Dictionary(texts_all)

# 输出每个词对应 的id
# print(dictionary.token2id)

# 一个文档中每行词对应的频率（ID，频率）
corpus = [dictionary.doc2bow(line) for line in texts_all]
# 一个文档中所有词对应的频率（合并list中的list元素）
print(sum((x if type(x)is list else [x] for x in corpus), []))

