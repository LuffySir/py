from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
import gensim
with open('E:\\dataset\\movie\\review_polarity\\txt_sentoken\\neg\\cv000_29416.txt','r') as f:
        texts = []
        for line in  f:
                ## print(line,end='')
                tokenizer = RegexpTokenizer(r'\w+')
                # “don’t” which will be read as two tokens, “don” and “t.”
                line_low = line.lower()
                tokens = tokenizer.tokenize(line_low)
                ## print(tokens)
                # create English stop words list
                en_stop = get_stop_words('en')
                # remove stop words from tokens
                stopped_tokens = [i for i in tokens if not i in en_stop]
                ## print(stopped_tokens)
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
ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=5, id2word = dictionary, passes=20)
print(ldamodel.print_topics(num_topics=5, num_words=1000))
