liebiao = [[1,2,3],[4,5],[6,7,8]]
dict_list = list()
for lb in liebiao:
    zidian = dict()
    for i in range(len(lb)):
        zidian[i] = lb[i]
    print(zidian)
    dict_list.append(zidian)
print(dict_list)
