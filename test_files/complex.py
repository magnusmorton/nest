print("This is a fairly complex nonsense epython program")

class Foo():
    def bar(self):
        return 345**3

    def looper(self):
        print("looper")
        a = [0]*10000
        # for elm in a:
        #     elm = 3
        
        b = [4]*10000
        for i in range(10000):
            a[i] = (b[i]) * 43
            b[i] = 10%3

        for i in range(10000):
            a[i]= (b[i])*43
            b[i] = 10%3
        for i in range(10000):
            a[i] = (b[i])*43
            b[i] = 10%3
        for i in range(10000):
            a[i] = (b[i])*43
            b[i] = 10%3
        for i in range(10000):
            a[i] = (b[i])*43
            b[i] = 10%3
        
        for i in range(10000):
            a[i] = (b[i])*43
            b[i] = 10%3
        for i in range(10000):
            a[i] = (b[i])*43
            b[i] = 10%3
        for i in range(10000):
            a[i] = (b[i])*43
            b[i] = 10%3
        for i in range(10000):
            a[i] = (b[i])*43
            b[i] = 10%3

        print("END")


Foo().looper()

        

        
