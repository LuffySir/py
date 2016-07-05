from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
import gensim
import os

tokenizer = RegexpTokenizer(r'\w+')

# 加停用词
en_stop = get_stop_words('en')

# 词干化
p_stemmer = PorterStemmer()

# 所有文件
path = 'E:\\dataset\\polar_movie\\all'
path2 = 'E:\\dataset\\polar_movie\\all2vec'
filelist = os.listdir(path)


# 循环遍历文档列表
for i in filelist:
    absfile = os.path.join(path, i)
    # 循环对每一个文档中的词标记
    texts = []
    with open(absfile, 'r') as file:
        for line in file:
            # print(line,end='')
            tokenizer = RegexpTokenizer(r'\w+')
            # “don’t” which will be read as two tokens, “don” and “t.”
            line_low = line.lower()
            tokens = tokenizer.tokenize(line_low)
            # print(tokens)
            # create English stop words list
            en_stop = get_stop_words('en')
            # remove stop words from tokens
            stopped_tokens = [i for i in tokens if not i in en_stop]
            # print(stopped_tokens)
            # Create p_stemmer of class PorterStemmer
            p_stemmer = PorterStemmer()
            # stem token
            stemmed_tokens = [p_stemmer.stem(i) for i in stopped_tokens]
            # print(texts)
            # add tokens to list
            texts.append(stemmed_tokens)

    dictionary = corpora.Dictionary(texts)
    # print(dictionary.token2id)
    corpus = [dictionary.doc2bow(text) for text in texts]
    # print(corpus)
    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=5, id2word=dictionary, passes=20)
    print(ldamodel.print_topics(num_topics=5, num_words=5))

    os.chdir(path2)
    f = open(i, 'w')
    for t in texts:
        for tt in t:
            f.write(tt)
            f.write("\n")
    f.close()
