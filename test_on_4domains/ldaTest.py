from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
import gensim
import re
import string

path1 = 'E:\\dataset\\domain_sentiment_data\\sorted_data_acl\\books\\review_text_neg'
path2 = 'E:\\dataset\\domain_sentiment_data\\sorted_data_acl\\books\\review_text_pos'
path3 = 'E:\\dataset\\en_stop_word'

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


def remvLowFreWord(corpora):
    wordNum = dict()
    for word in corpora:
        wordNum[word] = wordNum.get(word, 0) + 1
    low_wordNumList = []
    for word in wordNum.keys():
        if wordNum[word] < 11:
            low_wordNumList.append(word)

    print(len(wordNum))
    # print('book 词数',wordNum['book'])
    print(len(low_wordNumList))

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
corpus_after_process = []

# corpus 负向语料列表(1000个列表)，corpus_all_neg 负向语料列表（1000个元素）
corpus, corpus_all_neg = get_corpus(path1)
# corpus 所有语料列表(2000个列表)，corpus_all_pos 正向语料列表（1000个元素）
corpus, corpus_all_pos = get_corpus(path2)
# 所有语料（1个列表）
corpus_all = corpus_all_neg + corpus_all_pos

print(len(corpus_all))
print(len(corpus))

low_wordNumList = remvLowFreWord(corpus_all)
for item in corpus:
    item_remv_low = []
    for word in item:
            # 不在低频词列表中的词
        if not word in low_wordNumList:
            # item_remv_low.append(word)
            item_remv_low += word
    # 每一条评论的列表转换成字符串
    # review = ','.join(item_remv_low).replace(',', ' ')
    # 每一条评论构成列表的一个元素
    corpus_after_process.append(item_remv_low)

# print("corpus_after_process个数", len(corpus_after_process))
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
    count = 1
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
        # print("当前主题列表", topics)

        count += 1

    print(topics[0])
    print(topics[1])
    print(topics[2])
    print(topics[3])
    print(topics[4])
    print(len(topics[0]), len(topics[1]), len(topics[2]), len(topics[3]), len(topics[4]))
    return topics

topics_list = get_topic_set(5)
# for topic in ldamodel.print_topics(num_topics=5,num_words=10):
#     print(topic)
