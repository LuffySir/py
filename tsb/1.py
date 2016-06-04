def repp():

    a = ''
    b = 'allen'
    while(len(a+b) != 70):
        a = a + ' '
    print(a+b)
    print(len(a+b))

def print_twice(f,v):
    f()
    f()
    print(v)

print_twice(repp,2)
