class demo1:
    def met1(self):
        print("hello world")

class demo2(demo1):
    def met2(self):
        print("hello earth")

class demo3(demo2):
    def met3(self):
        print("hello india")

obj=demo3()
obj.met1()
obj.met2()
obj.met3()