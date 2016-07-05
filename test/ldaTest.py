from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
import gensim

tokenizer = RegexpTokenizer(r'\w+')

# create English stop words list
en_stop = get_stop_words('en')

# Create p_stemmer of class PorterStemmer
p_stemmer = PorterStemmer()

# create sample documents
doc_a = "Brocolli is good to eat. My brother likes to eat good brocolli, but not my mother."
doc_b = "My mother spends a lot of time driving my brother around to baseball practice."
doc_c = "Some health experts suggest that driving may cause increased tension and blood pressure."
doc_d = "I often feel pressure to perform well at school, but my mother never seems to drive my brother to do better."
doc_e = "Health professionals say that brocolli is good for your health."

# compile sample documents into a list
doc_set = [doc_a, doc_b, doc_c, doc_d, doc_e]

# list for tokenized documents in loop
texts = []

# loop through document list
for i in doc_set:

    # clean and tokenize document string
    raw = i.lower()
    tokens = tokenizer.tokenize(raw)

    # remove stop words from tokens
    stopped_tokens = [i for i in tokens if not i in en_stop]

    # stem tokens
    stemmed_tokens = [p_stemmer.stem(i) for i in stopped_tokens]

    # add tokens to list
    texts.append(stemmed_tokens)

# print(texts[1])

# turn our tokenized documents into a id <-> term dictionary
dictionary = corpora.Dictionary(texts)

# convert tokenized documents into a document-term matrix
corpus = [dictionary.doc2bow(text) for text in texts]

# tfidf = models.TfidfModel(corpus)
# corpus_tfidf = tfidf[corpus]

# generate LDA model
ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=5, id2word=dictionary, passes=20)


# def get_topic_set(num):
#     topics = list()
#     # [[],[]……]
#     for i in range(num):
#         topics.append(list())
#     # 初始化文档编号
#     count = 1
#     # cor文档集中文档对应的词袋向量
#     for cor in corpus:
#         # print(ldamodel[cor])
#         # 文档对应的主题，概率元祖
#         for tup in ldamodel[cor]:
#             # 主题，概率
#             topic, prob = tup
#             print("文档编号", count)
#             print(topic, prob)
#             if prob >= 0.95:
#                 print("主题概率大于0.4的文档编号", count)
#                 # print(topic, prob)
#                 # 主题概率大于0.4的文档编号加入到相应的列表中
#                 topics[topic].append(count)
#             # elif prob >= 0.01:  # 1 / num:
#                 # max_prob = prob
#                 # max_prob = getMaxProb(prob, max_prob)
#                 # topics[topic].append(count)
#                 # for i in range(num):
#                 #     for j in range(len(cor)):
#                 #         max_prob = max(tup[i][j])
#         # print("最大概率", max_prob)
#         count += 1

#     print(topics[0], topics[1])
#     return topics

def get_topic_set(num):
    topics = list()
    # [[],[]……]
    for i in range(num):
        topics.append(list())
    # 初始化文档编号
    count = 1
    # cor文档集中文档对应的词袋向量
    for cor in corpus:
        prob_list = list()
        print("元祖", ldamodel[cor])
        for i in range(num):
            print(ldamodel[cor][i])
            prob_list.append(ldamodel[cor][i][1])
            if ldamodel[cor][i][1] >= 0.95:
                topics[ldamodel[cor][i][0]].append(count)
                # print("当前主题列表", topics)
        # print("概率列表", prob_list)
        max_prob = max(prob_list)
        print("最大概率", max_prob)
        if (count not in topics[prob_list.index(max_prob)]):
            topics[prob_list.index(max_prob)].append(count)
        print("当前主题列表", topics)

        count += 1

    print(topics)
    return topics

get_topic_set(5)


# for topic in ldamodel.print_topics(num_topics=3,num_words=10):
#     print(topic)
