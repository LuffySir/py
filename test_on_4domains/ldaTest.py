from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
import gensim
import re
import string
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer

path1 = 'E:\\dataset\\domain_sentiment_data\\sorted_data_acl\\books\\review_text_neg'
path2 = 'E:\\dataset\\domain_sentiment_data\\sorted_data_acl\\books\\review_text_pos'
path3 = 'E:\\dataset\\en_stop_word'
path_str = 'E:\\dataset\\domain_sentiment_data\\sorted_data_acl\\books\\topic_tfidf\\review_text_tfidf_topic'
path4 = 'E:\\dataset\\domain_sentiment_data\\sorted_data_acl\\books\\topic_tfidf\\label_list'

tokenizer = RegexpTokenizer(r'\w+')

# 加停用词
en_stop = get_stop_words('en')
with open(path3, 'r') as en_stop_f:
    for line in en_stop_f:
        line = line.strip()
        en_stop.append(line)

# en_stop.append('don')
en_stop.append('_the')
en_stop.append('book')
en_stop.append('read')
en_stop.append('time')
en_stop.append('people')

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


def remvLowFreWord(all_corpora):
    wordNum = dict()
    for word in all_corpora:
        wordNum[word] = wordNum.get(word, 0) + 1
    low_wordNumList = []
    for word in wordNum.keys():
        if wordNum[word] < 11:
            low_wordNumList.append(word)

    print('词数', len(wordNum))    # 15135
    # print('book 词数',wordNum['book'])
    print('低频词数', len(low_wordNumList))    # 12879

    return low_wordNumList


def get_corpus(path):
    corpus_all_x = []
    with open(path, 'r') as f:
        for line in f:
                # 对每一条评论进行预处理,得到的是列表
            lineTokens = stemmer(line)
            # 预处理后的每一条评论添加到语料库列表中
            corpus_all_x = corpus_all_x + lineTokens
            # 预处理后的每一条评论添加到语料库列表中（列表的列表）
            corpus.append(lineTokens)
    return corpus, corpus_all_x

corpus = []
# 用于lda计算,列表的列表[[xx,xx,xx],[yy,yy]...]
corpus_after_process = []
# 用于tfidf计算，列表[xx,yy...]
corpus_after_process_tf = []

# corpus 负向语料列表(1000个列表)，corpus_all_neg 负向语料列表（1000个元素）
corpus, corpus_all_neg = get_corpus(path1)
# corpus 所有语料列表(2000个列表)，corpus_all_pos 正向语料列表（1000个元素）
corpus, corpus_all_pos = get_corpus(path2)
# 所有语料（1个列表）
corpus_all = corpus_all_neg + corpus_all_pos

# print(len(corpus_all))    # 126686
# print(len(corpus))    # 2000
# print(corpus[1])   #corpus[i]是列表

low_wordNumList = remvLowFreWord(corpus_all)
for item in corpus:
    item_remv_low = []
    for word in item:
            # 不在低频词列表中的词
        if not word in low_wordNumList:
            item_remv_low.append(word)
            # item_remv_low += word
    # 每一条评论的列表转换成字符串
    review = ','.join(item_remv_low).replace(',', ' ')
    # 每一条评论构成列表的一个列表元素
    corpus_after_process.append(item_remv_low)
    # 每一条评论构成列表的一个元素
    corpus_after_process_tf.append(review)

print("corpus_after_process个数", len(corpus_after_process))
print(corpus_after_process[1])
print("corpus_after_process_tf个数", len(corpus_after_process_tf))
print(corpus_after_process_tf[1])

dictionary = corpora.Dictionary(corpus_after_process)
cor = [dictionary.doc2bow(review) for review in corpus_after_process]

ldamodel = gensim.models.ldamodel.LdaModel(cor, num_topics=5, id2word=dictionary, passes=20, minimum_probability=0.0001)


def get_topic_set(num):
    topics = list()
    # [[],[]……]
    for i in range(num):
        topics.append(list())
    # print(topics)
    # 初始化文档编号
    count = 0
    # c:文档集中文档对应的词袋向量
    for c in cor:
        # 概率值列表
        prob_list = list()
        # print("元祖", ldamodel[c])
        # i表示第几个元祖(主题，概率)
        for i in range(num):
            # print(ldamodel[c][i])
            # 概率值加入到概率值列表
            prob_list.append(ldamodel[c][i][1])
            # 如果概率值大于0.4，加入到相应的集合中
            if ldamodel[c][i][1] >= 0.4:
                topics[ldamodel[c][i][0]].append(count)
                # print("当前主题列表", topics)
        # print("概率列表", prob_list)
        max_prob = max(prob_list)
        # print("最大概率", max_prob)
        # 概率最大的，也加入到相应的集合中
        if (count not in topics[prob_list.index(max_prob)]):
            topics[prob_list.index(max_prob)].append(count)

        count += 1

    return topics


def get_label(topic_num, label_path_base):

    for j in range(topic_num):
        label_path = label_path_base + str(j)
        with open(label_path, 'w') as labelFile:

            for i in range(len(topics_list[j])):
                labelFile.write(str(topics_list[j][i]))
                labelFile.write(' ')
                # 大于1000的是正向
                if topics_list[j][i] >= 1000:
                    labelFile.write('1')
                else:
                    labelFile.write('0')
                labelFile.write('\n')



def get_topic_tfidf(cor_list, topic_num, path_base):
    # 该类将文本中的词语转换成词频矩阵，矩阵元素a[i][j]表示词j在第i个文本下的词频
    vectorizer = CountVectorizer()
    # 统计每个词语的tfidf
    transformer = TfidfTransformer()

    corpus_split = list()

    for i in range(topic_num):
        corpus_split.append(list())
        for j in topics_list[i]:
            # 把评论放到相应主题下的列表中
            corpus_split[i].append(cor_list[j])
        print('第', i, '个列表元素的长度', len(corpus_split[i]))

        # 第一个fit_transformer是计算tfidf，第二个是转化成词频矩阵
        tfidf = transformer.fit_transform(
            vectorizer.fit_transform(corpus_split[i]))
        # 获取词袋模型中的所有词语
        word = vectorizer.get_feature_names()
        # 将tfidf矩阵抽取出来，a[i][j]表示词j在第i个文本中的tfidf权重
        weight = tfidf.toarray()

        path = path_base + str(i)

        with open(path, 'w') as f:
            for m in range(len(weight)):
                for n in range(len(word)):
                    # f.write(word[n])
                    # f.write(' ')
                    f.write(str(weight[m][n]))
                    f.write(' ')
                f.write('\n')

topics_list = get_topic_set(5)

get_label(5, path4)

get_topic_tfidf(corpus_after_process_tf, 5, path_str)
