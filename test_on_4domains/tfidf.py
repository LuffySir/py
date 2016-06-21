from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
import string
import re

path1 = 'E:\\dataset\\domain_sentiment_data\\sorted_data_acl\\books\\review_text_neg'
path2 = 'E:\\dataset\\domain_sentiment_data\\sorted_data_acl\\books\\review_text_pos'
path3 = 'E:\\dataset\\domain_sentiment_data\\sorted_data_acl\\books\\review_text_tfidf'

tokenizer = RegexpTokenizer(r'\w+')

# 加停用词
en_stop = get_stop_words('english')

# 词干化
p_stemmer = PorterStemmer()


def stemmer(line):
    line = re.sub(r'([\d]+)', '', line)
    line_low = line.lower()
    tokens = tokenizer.tokenize(line_low)
    stopped_tokens = [i for i in tokens if not i in en_stop]
    stopped_tokens = [i for i in stopped_tokens if not i in string.digits]
    stopped_tokens = [i for i in stopped_tokens if not len(i) < 3]
    stemmed_tokens = [p_stemmer.stem(i) for i in stopped_tokens]

    return stemmed_tokens


def remvLowFreWord(corpora):
    wordNum = dict()
    for word in corpora:
        wordNum[word] = wordNum.get(word, 0) + 1
    low_wordNumList = []
    for word in wordNum.keys():
        if wordNum[word] < 11:
            low_wordNumList.append(word)

    return low_wordNumList


def get_corpus(path):
    corpus_all_x = []
    with open(path, 'r') as f:
        for line in f:
            lineTokens = stemmer(line)
            corpus_all_x = corpus_all_x + lineTokens
            corpus.append(lineTokens)
    return corpus, corpus_all_x


def get_tfidf(path):
    
    corpus, corpus_all_neg = get_corpus(path1)
    corpus, corpus_all_pos = get_corpus(path2)
    corpus_all = corpus_all_neg + corpus_all_pos
    print(len(corpus))
    print(len(corpus_all))
    low_wordNumList = remvLowFreWord(corpus_all)
    for item in corpus:
        item_remv_low = []
        for word in item:
            if not word in low_wordNumList:
                item_remv_low.append(word)
        review = ','.join(item_remv_low).replace(',', ' ')
        corpus_after_process.append(review)

    print(corpus_after_process[1001])

    # 该类将文本中的词语转换成词频矩阵，矩阵元素a[i][j]表示词j在第i个文本下的词频
    vectorizer = CountVectorizer()
    # 统计每个词语的tfidf权值
    transformer = TfidfTransformer()
    # 第一个fit_transformer是计算tfidf，第二个是转化成词频矩阵
    tfidf = transformer.fit_transform(
        vectorizer.fit_transform(corpus_after_process))
    # 获取词袋模型中的所有词语
    word = vectorizer.get_feature_names()
    # 将tfidf矩阵抽取出来，a[i][j]表示词j在第i个文本中的tfidf权重
    weight = tfidf.toarray()
    with open(path, 'w') as f:
        for i in range(len(weight)):
            for j in range(len(word)):
                f.write(word[j])
                f.write(' ')
                f.write(str(weight[i][j]))
                f.write(' ')
            f.write('\n')


corpus = []
corpus_after_process = []
# corpus_all = []
get_tfidf(path3)
