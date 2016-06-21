#-*- coding:utf-8 -*-
import re
import string

path1 = 'E:\\dataset\\domain_sentiment_data\\sorted_data_acl\\books\\negative.review'
path2 = 'E:\\dataset\\domain_sentiment_data\\sorted_data_acl\\books\\review_text_neg'
path3 = 'E:\\dataset\\domain_sentiment_data\\sorted_data_acl\\books\\review_score_neg'

path4 = 'E:\\dataset\\domain_sentiment_data\\sorted_data_acl\\books\\positive.review'
path5 = 'E:\\dataset\\domain_sentiment_data\\sorted_data_acl\\books\\review_text_pos'
path6 = 'E:\\dataset\\domain_sentiment_data\\sorted_data_acl\\books\\review_score_pos'

def extarctContent(pathIn, pathOut, pathOutScore):

	with open(pathIn, 'r', encoding="utf-8-sig") as fs:
		match = re.findall(r'<rating>(.*?)</rating>', fs.read(), re.S)
		scoreFile = open(pathOutScore, 'w')
		for item in match:
			item2str = str(item.encode("GBK", 'ignore'))
			item2str = item2str[4:]
			item2str = item2str[:-3]
			scoreFile.write(item2str)
			scoreFile.write('\n')
		scoreFile.close()

	with open(pathIn,'r',encoding="utf-8-sig") as f:
		match = re.findall(r'<review_text>(.*?)</review_text>',f.read(),re.S)
		reviewFile = open(pathOut,'w')
		for item in match:
			item.strip()
			item2str = str(item.encode("GBK", 'ignore'))
			item2str = item2str[4:]
			item2str = item2str[:-3]
			item2str = item2str.strip()
			item2str = item2str.replace('\\','')
			item2str = item2str.replace('\\n','')
			reviewFile.write(item2str)
			reviewFile.write('\n')
		reviewFile.close()


extarctContent(path1, path2, path3)
extarctContent(path4, path5, path6)
