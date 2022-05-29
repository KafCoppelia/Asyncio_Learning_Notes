'''
    迭代器必须同时实现__next__和__iter__两个方法，称为迭代器协议
    所有迭代器的__iter__方法都只需要return self即可
    *并不是所有的可迭代对象都必须定义__iter__方法，__getitem__也可以
    -> 不能通过检查__iter__方法判断一个对象是否可迭代，应使用iter()，若不可迭代抛出TypeError
'''
class MyIterator:
    def __init__(self, actions):
        self.actions = actions
        self.index = 0

    def __next__(self):
        while self.index < len(self.actions):
            action = self.actions[self.index]
            self.index += 1
        
        raise StopIteration
        
    def __iter__(self):
        return self

'''
    迭代器意义：
    - 1 统一通过next()方法获取数据，屏蔽底层不同的数据读取方式
    - 2 容器类的数据结构之关系数据的静态存储，每一次迭代都需要额外的迭代器对象专门负责记录迭代过程中的状态信息
    - 3 一个可迭代对象可以构建任意多个不同的迭代器
    - 4 一种迭代器可以应用于任意多个可迭代对象（包括其他迭代器）
'''
# 迭代器构建数据管道、数据生成器(Generator)，例如
from random import random

class Random:
    def __iter__(self):
        return self
    
    def __next__(self):
        return random() # 无穷迭代，每次数据都是实时产生的，不占用内存空间
