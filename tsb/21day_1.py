import linecache

score_path_base = 'E:\\dataset\\domain_sentiment_data\\sorted_data_acl\\books\\topic_score\\score_list'
label_path_base = 'E:\\dataset\\domain_sentiment_data\\sorted_data_acl\\books\\topic_tfidf_label\\label_list'
score = 'E:\\dataset\\domain_sentiment_data\\sorted_data_acl\\books\\review_score'

for i in range(5):
    label_path = label_path_base + str(i)
    score_path = score_path_base + str(i)
    with open(label_path, 'r') as label_file:
        with open(score_path, 'w') as score_file:
            for line in label_file:
                line = line.strip()
                line_num = int(line[:-2])
                topic_score_list = linecache.getline(score, line_num + 1)
                score_file.write(topic_score_list[0])
                score_file.write('\n')
