print("This is a fairly complex nonsense epython program")

class Foo():
    def bar(self):
        return 345**3

    def looper(self):
        a = [0]*1000
        # for elm in a:
        #     elm = 3
        
        b = [4]*1000
        for i in range(1000):
            a[i] = (b[i]) * 43
            b[i] = 10%3

        for i in range(1000):
            a[i]= (b[i])*43
            b[i] = 10%3
        for i in range(1000):
            a[i] = (b[i])*43
            b[i] = 10%3
        for i in range(1000):
            a[i] = (b[i])*43
            b[i] = 10%3
        for i in range(1000):
            a[i] = (b[i])*43
            b[i] = 10%3
        
        for i in range(1000):
            a[i] = (b[i])*43
            b[i] = 10%3
        for i in range(1000):
            a[i] = (b[i])*43
            b[i] = 10%3
        for i in range(1000):
            a[i] = (b[i])*43
            b[i] = 10%3
        for i in range(1000):
            a[i] = (b[i])*43
            b[i] = 10%3


Foo().looper()

        

        
