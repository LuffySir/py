import string
import os

path = 'E:\\dataset\\polar_movie\\test'

hist = dict()

def process_file(filename):
    
    fp = open(filename)
    for line in fp:
        process_line(line,hist)
    return hist

def process_line(line,hist):
    # line = line.replace('-',' ')

    for word in line.split():
        word = word.strip(string.punctuation + string.whitespace)
        word = word.lower()

        hist[word] = hist.get(word,0) + 1

# 总词数
def total_words(hist):
    return sum(hist.values())

# 不同词语的个数
def diff_words(hist):
    return len(hist)

# 最常用的单词
def most_common(hist):
    t = []
    for key,value in hist.items():
        t.append((value,key))

    t.sort(reverse = True)
    return t

# 字典减法
def subtract(d1,d2):
    res = dict()
    for key in d1:
        if key not in d2:
            res[key] = None    #########
    return res

filelist = os.listdir(path)

for i in filelist:
    absfile = os.path.join(path,i);
    hist = process_file(absfile)
    # print(total_words(hist))
# print(hist)
print(total_words(hist))
print(diff_words(hist))
t = most_common(hist)
for fre,word in t[0:10]:
    print (word,'\t',fre)
