from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import PorterStemmer
import linecache
import math


# pos word
pos_path = 'E:\\dataset\\senti_word_test\\pos.txt'
# neg word
neg_path = 'E:\\dataset\\senti_word_test\\neg.txt'

most_path = 'E:\\dataset\\senti_word_test\\most'
very_path = 'E:\\dataset\\senti_word_test\\very'
more_path = 'E:\\dataset\\senti_word_test\\more'
ish_path = 'E:\\dataset\\senti_word_test\\ish'
insufficient_path = 'E:\\dataset\\senti_word_test\\insufficient'
inverse_path = 'E:\\dataset\\senti_word_test\\inverse'

path1 = 'E:\\dataset\\domain_sentiment_data\\sorted_data_acl\\electronics\\review_text_neg'
path2 = 'E:\\dataset\\domain_sentiment_data\\sorted_data_acl\\electronics\\review_text_pos'

neg_score_path = 'E:\\dataset\\domain_sentiment_data\\sorted_data_acl\\electronics\\neg_cal_score'
pos_score_path = 'E:\\dataset\\domain_sentiment_data\\sorted_data_acl\\electronics\\pos_cal_score'

score_neg = 'E:\\dataset\\domain_sentiment_data\\sorted_data_acl\\electronics\\review_score_neg'
score_pos = 'E:\\dataset\\domain_sentiment_data\\sorted_data_acl\\electronics\\review_score_pos'

tokenizer = RegexpTokenizer(r'\w+')

# Create p_stemmer of class PorterStemmer
p_stemmer = PorterStemmer()


def get_word_dict(dict_file):

    word_list = []

    with open(dict_file, 'r') as dFile:
        for word in dFile:
            word_low = word.lower()
            word_low = word_low.strip()
            tokens = tokenizer.tokenize(word_low)
            line = ','.join(tokens).replace(',', ' ')
            word_list.append(line)

    return word_list


def match(word, sentiment_value):
    if word in mostdict:
        sentiment_value *= 5
    elif word in verydict:
        sentiment_value *= 4
    elif word in moredict:
        sentiment_value *= 3
    elif word in ishdict:
        sentiment_value *= 2
    elif word in insufficientdict:
        sentiment_value *= 1

    return sentiment_value


def match_inverse(word, sentiment_value):
    if word in inversedict:
        sentiment_value *= -1
    return sentiment_value


def cal_review_score(review):

    # 评论中词的位置
    i = 0

    pos_all = 0
    neg_all = 0
    for i in range(len(review)):
        # 每次把情感词分数归零
        pos_score = 0
        if review[i] in posdict:
            pos_score += 1
            # 情感词前3个词内有表示程度的词则乘以相应的系数
            j = i - 4
            for j in range(i + 4):
                if (j < len(review)) and (j >= 0):
                    pos_score = match(review[j], pos_score)
                if pos_score > 2:
                    break

            # 情感词前3个词内有表示程度的词则乘以相应的系数
            j = i - 10
            for j in range(i + 0):
                if (j < len(review)) and (j >= 0):
                    pos_score = match_inverse(review[j], pos_score)

        # 情感词分数加到评论分数中
        pos_all += pos_score

        neg_score = 0
        if review[i] in negdict:
            neg_score += 1
            j = i - 4
            for j in range(i + 4):
                if (j < len(review)) and (j >= 0):
                    neg_score = match(review[j], neg_score)
                if neg_score > 2:
                    break

            j = i - 10
            for j in range(i + 0):
                if (j < len(review)) and (j >= 0):
                    neg_score = match_inverse(review[j], neg_score)

        neg_all += neg_score

    return pos_all, neg_all


def get_review_score(review, star, k):

    review_score = 0
    pos, neg = cal_review_score(review)
    if k <= 3:
        print(pos, neg)
    if float(star) == 5.0:
        review_score = math.floor(pos * 0.9 - neg * 0.1) + 5
    elif float(star) == 4.0:
        review_score = math.floor(pos * 0.7 - neg * 0.3) + 3
    elif float(star) == 2.0:
        review_score = math.floor(pos * 0.3 - neg * 0.7) - 3
    elif float(star) == 1.0:
        review_score = math.floor(pos * 0.1 - neg * 0.9) - 5

    return review_score


def get_score_file(rev_file, score_file, score_path):
    p_count = 0
    n_count = 0
    z_count = 0
    # 评论序号
    k = 1
    with open(rev_file, 'r') as rFile:
        with open(score_file, 'w') as wfile:
            # with open(score_path, 'r') as sfile:
            for review in rFile:
                review_low = review.lower()
                review_low = review_low.strip()
                # review_low = review_low.replace('\'t', ' not')
                review_tokens = tokenizer.tokenize(review_low)
                # review_str = ','.join(review_tokens).replace(',', ' ')
                # 该评论的星级评分
                star = linecache.getline(score_path, k)

                review_score = get_review_score(review_tokens, star, k)
                if k <= 3:
                    print(star)
                    print(review_score)
                if review_score > 0:
                    p_count += 1
                elif review_score < 0:
                    n_count += 1
                else:
                    z_count += 1
                wfile.write(str(review_score))
                wfile.write('\n')
                k += 1
    print('正：', p_count)
    print('负：', n_count)
    print('零：', z_count)

posdict = get_word_dict(pos_path)
negdict = get_word_dict(neg_path)
mostdict = get_word_dict(most_path)
verydict = get_word_dict(very_path)
moredict = get_word_dict(more_path)
ishdict = get_word_dict(ish_path)
insufficientdict = get_word_dict(insufficient_path)
inversedict = get_word_dict(inverse_path)

print("消极")
get_score_file(path1, neg_score_path, score_neg)
print("============")
print("积极")
get_score_file(path2, pos_score_path, score_pos)
