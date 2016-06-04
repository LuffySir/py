from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
import gensim
import string
import os

# pos word
pos_path = 'E:\\dataset\\sentiment word\\pos.txt'
# neg word
neg_path = 'E:\\dataset\\sentiment word\\neg.txt'
# write in new file
new_pos_path = 'E:\\dataset\\sentiment word\\pos_stem.txt'
new_neg_path = 'E:\\dataset\\sentiment word\\neg_stem.txt'

tokenizer = RegexpTokenizer(r'\w+')

# create English stop words list
en_stop = get_stop_words('en')

# Create p_stemmer of class PorterStemmer
p_stemmer = PorterStemmer()

def stemmer(file,newfile):
    stemmed_tokens_nosame = []
    fin = open(newfile,'w')
    with open(file,'r') as file:
        for line in file:
            line_low = line.lower()
            tokens = tokenizer.tokenize(line_low)
            
            stopped_tokens = [i for i in tokens if not i in en_stop]
            stopped_tokens = [i for i in stopped_tokens if not i in string.digits]
            stopped_tokens = [i for i in stopped_tokens if not len(i)<2]
            
            stemmed_tokens = [p_stemmer.stem(i) for i in stopped_tokens]
            
            if not stemmed_tokens in stemmed_tokens_nosame:
                stemmed_tokens_nosame.append(stemmed_tokens)
        fin.write(str(stemmed_tokens_nosame))

    fin.close()

stemmer(pos_path,new_pos_path)  
#stemmer(neg_path,new_neg_path)
