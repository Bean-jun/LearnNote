# https://lotabout.me/2020/C3-Algorithm/
class A():
    def say(self):
        print("A say")
class B(A):
    pass
class C():
    def say(self):
        print("C say")
class D(B, C):
    pass

d=D()
d.say()
print(D.__mro__)