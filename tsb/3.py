import math

def print_m():
    print('m')

def do_n(f,n):
    if n <= 0:
        return
    f()
    do_n(f,n-1)

do_n(print_m,4)
    


def hhh(a,b):
	m = a**2 + b**2
	c = math.sqrt(m)

	print (c)
	return c

hhh(3,4)

def f(n):
    if n == 0:
        return 1
    else:
        recurse = f(n-1)
        res = n*recurse
        print(res)
        return res
f(3)
    
    
    
