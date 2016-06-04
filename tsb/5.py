def sum_list(t):
    m = len(t)
    index = 0
    while index < m:
        if index == 0:
            t[index] = t[index]
            
        else:
            t[index] = t[index] + t[index-1]
        index += 1
    print(t)

    return t

sum_list([1,2,3,4])        
