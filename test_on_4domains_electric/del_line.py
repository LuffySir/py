path_in = 'E:\\dataset\\senti_word_test\\neg.txt'
path_out = 'E:\\dataset\\senti_word_test\\neg_new.txt'
with open(path_in, 'r') as rfile:
    with open(path_out, 'w') as wfile:
        for line in rfile:
            if len(line) < 18:
                wfile.write(line)
