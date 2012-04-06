a = [0]*100000
b = [0]*100000
for i in range(10000):
    a[i] = i**3 + 2*i -12
    b[i] = 345-i+ 12

assert a[1] is not 0
