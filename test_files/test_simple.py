
def loop():
    a = [0]*10000
    foo()
    for i in range(10000):
        a[i] = 2*3 + 45
    print(a)

loop()

def foo():
    print("hello")

