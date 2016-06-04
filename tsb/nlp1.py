from nltk.book import *

fdist = FreqDist(text1)
vocalbulary = list(fdist)
print(vocalbulary[:10])
