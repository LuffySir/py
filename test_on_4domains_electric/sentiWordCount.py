from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import PorterStemmer


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
        sentiment_value *= 1
    if word in verydict:
        sentiment_value *= 1
    if word in moredict:
        sentiment_value *= 1
    if word in ishdict:
        sentiment_value *= 0.5
    if word in insufficientdict:
        sentiment_value *= 0.25
    if word in inversedict:
        sentiment_value *= -1
    return sentiment_value


def get_review_score(review):

    review_score = 0
    # 评论中词的位置
    i = 0

    for i in range(len(review)):
        # 每次把情感词分数归零
        pos_score = 0
        if review[i] in posdict:
            pos_score += 1
            # 情感词前3个词内有表示程度的词则乘以相应的系数
            j = i - 3
            for j in range(i + 3):
                if (j < len(review)) and (j >= 0):
                    pos_score = match(review[j], pos_score)
                j += 1

        # 情感词分数加到评论分数中
        review_score += pos_score

        neg_score = 0
        if review[i] in negdict:
            neg_score += 1
            j = i - 3
            for j in range(i + 3):
                if (j < len(review)) and (j >= 0):
                    neg_score = match(review[j], neg_score)
                j += 1

        review_score -= neg_score

        i += 1

    return review_score


def get_score_file(rev_file, score_file):
    p_count = 0
    n_count = 0
    z_count = 0
    with open(rev_file, 'r') as rFile:
        with open(score_file, 'w') as wfile:
            for review in rFile:
                review_low = review.lower()
                review_low = review_low.strip()
                review_tokens = tokenizer.tokenize(review_low)
                # review_str = ','.join(review_tokens).replace(',', ' ')
                review_score = get_review_score(review_tokens)
                if review_score > 0:
                    p_count += 1
                elif review_score < 0:
                    n_count += 1
                else:
                    z_count += 1
                wfile.write(str(review_score))
                wfile.write('\n')
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

get_score_file(path1, neg_score_path)
get_score_file(path2, pos_score_path)
