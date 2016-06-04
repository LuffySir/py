def hh(s):
    d = dict()
    for c in s:
        #若c在字典的键中，返回对应的值，否则返回默认值0
        d[c] = d.get(c,0)+1 
    print (d)
    return d

hh('hdfkhasldf')
