'''
Created on: ********

Author: Yi Zheng, Department of Electrical Engineering, DTU

Some confused syntax is tested in this file.
'''

# Understanding multiple inheritance
# class Base(object):
#     def __init__(self):
#         print ("enter Base")
#         print ("leave Base")
# 
# class A(Base):
#     def __init__(self):
#         print ('enter A')
#         Base().__init__()
#         print ('leave A')
# 
# class B(Base):
#     def __init__(self):
#         print ('enter B')
#         Base().__init__()
#         print ('leave B')
# 
# class C(A, B):
#     def __init__(self):
#         print ('enter C')
#         A().__init__()
#         B().__init__()
#         print ('leave C')

class Base(object):
    def __init__(self):
        print ("enter Base")
        print ("leave Base")

class A(Base):
    def __init__(self):
        print ('enter A')
        super().__init__()
        print ('leave A')

class B(Base):
    def __init__(self):
        print ('enter B')
        super().__init__()
        print ('leave B')

class C(A, B):
    def __init__(self):
        print ('enter C')
        super(C, self).__init__()
        print ('leave C')

if __name__ == '__main__':
    test = 1
    if test == 1:
        # Multiple inheritance
        C()
    elif test == 2:
        # lambda function lambda arguments: return value
        plus_one = lambda x: x + 1
        print(plus_one(3))
        # This is not a good way to define a function. It should only be used when you don't need a named function.
