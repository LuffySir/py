#-*- coding:utf-8 -*-
ll = ['you and me','she ans her','go to bed']
wordNum = dict()

for word in ll:
	wordNum[word] = wordNum.get(word,0) + 1
	print("词频",word,wordNum[word])
