'''
    通常含有yield的函数称为“生成器函数”，把调用生成器函数返回的结果称为生成器
    
    yield对函数做了什么：
    最根本的作用是改变了函数的性质：
    - 1 调用生成器函数不是直接执行其中的代码，而是返回一个对象；
    - 2 生成器函数内的代码，需要通过生成器对象来执行（和类差不多）；
    
    只遭遇一次yield语句的生成器就是只能迭代一次的迭代器，无实际加之；可在函数内多次使用/搭配循环
'''

def count(start=0, step=1):
    n = start
    while True:
        yield n
        n += step

c = next(count(10))  
print(c)

'''
    生成器的4个状态：
    - 1 当调用生成器函数得到生成器对象时，此时可理解为处于初始状态
    - 2 通过next()调用声称其对象，对应的生成器函数代码运行，此时处于运行中状态
    - 3 若遇到yield，next()返回时：
        - 1 yield语句右边的对象作为返回值
        - 2 生成器在yield语句所在的位置暂停，当在此使用next()时继续从该位置运行
    - 4 若执行到函数结束，抛出StopIteration：
        - 1 不管是否使用return显式地返回，或默认返回None，返回值都只能作为异常值一并抛出
        - 2 此时生成器对象处于结束状态
        - 3 对于已结束的生成器对象再次调用next()，直至抛出StopIteration，并不含返回值
'''

'''
    用yield重构迭代器
    和class定义的迭代器对比：
    - 1 定义迭代器：
        - 1 Class:
            class Iterator:
                def __init__(self, *args)
        - 2 yield:
            def iter_fun(*args):...
    - 2 构建迭代器：
        - 1 Iterator(args)
        - 2 iter_func(args)
    - 3 next:
        - 1 def __next__(self): return value
        - 2 yield value
    - 4 StopIteration
        - 1 raise StopIteration
        - 2 return
    - 5 iter(iterator)
        - 1 def __iter__(self): return self
        - 2 自动实现
    
    应用场景：
    - 1 定义一个容器类的可迭代对象，为该对象实现__iter__接口
    - 2 定义一个处理其他可迭代对象的迭代器
    - 3 定义一个不依赖数据存储的数据生成器
    
    e.g.1:
'''
class MyCustomDataIterator:
    def __init__(self, data):
        self.data = data
        self.index = -1

    def __next__(self):
        self.index += 1
        if self.index < self.data.size:
            return self.data.get_value(self.index)
        else:
            raise StopIteration
        
    def __iter__(self):
        return self

# 可迭代数据类
class MyCustomData:
    ...
    @property
    def size(self):             # 假设可以得到数据大小
        return self.size

    def get_value(self, index): # 假设可通过索引按顺序得到数据
        return index
    
    def __iter__(self):
        return MyCustomDataIterator(self)   # 构建迭代器

'''
    e.g.1改yield写法
'''
class MyCustomData:
    ...
    @property
    def size(self):             # 假设可以得到数据大小
        return self.size

    def get_value(self, index): # 假设可通过索引按顺序得到数据
        return index
    
    def __iter__(self):
        index = -1              # 局部变量！
        while index < 2:        # 设置迭代完成条件
            index += 1
            yield self.get_value(index)
            
mydata = MyCustomData() # 注意：mydata是可迭代对象，但不是迭代器

'''
    - 2 实现有数据处理能力的迭代器
    e.g.2:
'''
def deal(actions):
    for action in actions:
        if action == "A":
            continue
        elif "B" in action:
            yield action * 2
        else:
            yield action
            
actions = ["AA", "CC", "BBB"]
for x in deal(actions):
    print(x)

'''
    - 3 实现一个数据生成器
    e.g.3:
'''
class CountDown:
    def __init__(self, start):
        self.start = start
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.start > 0:
            self.start -= -1
            return self.start
        else:
            raise StopIteration
'''
    改yield
'''        
def countdown(start):
    while start > 0:
        start -= 1
        yield start

for x in countdown(5):
    print(x)

'''
    生成器 -> 协程
'''
# 函数对象和代码对象：函数中的代码时保存在代码对象中的
def func():
    x = 1
    print(x)
    
func.__code__

# 帧对象保存函数运行时的状态，每次调用函数均自动创建帧对象，记录档次运行状态
import inspect
def foo():
    return inspect.currentframe()

f1 = foo()
f1
f2 = foo()

'''
    函数运行帧/栈帧：
    - 1 函数之间的调用关系是先执行的后退出，帧对象之间的关系也是先入后出，以栈的形式保存
    - 2 一个线程只有一个函数运行帧
'''

'''
    生成器函数有何不同：
    - 1 仍是函数对象，也包括代码对象
    - 2 调用生成器函数不会直接运行，而是得到生成器对象
        - 1 每次使用next()调用生成器时，就是将生成器引用的帧对象入栈
        - 2 当next()返回时，也就是遇到yield暂停时，将帧出栈
        - 3 直到迭代结束，帧最后一次出栈，并被销毁
        
    让一个函数可以多次迭代运行其中的代码才是生成器对象最根本的作用，迭代产出数据知识迭代执行代码的自然结果
''' 

'''
    yield表达式，意味着可以被解析成一个值，但仍只能用在函数内
'''
def show_yield_value():
    print("Start")
    x = yield
    print(f"x is {x}")

g = show_yield_value()
g.send(None)    # 对刚创建好的生成器，第一次只能send None
g.send("Hello")

'''
    对刚创建好的生成器，总需要在第一次的时候Send None值，使其运行到yield时暂停，这个步骤术语为prime
    
    yield表达式的优先级
'''
def add_yield_value():
    # x = yield + 1
    x = (yield) + 1
    print(f"x is {x}")

g = add_yield_value()
g.send(None)
g.send(1)

'''
    - 1 send 是生成器对象的方法
    - 2 对于生成器对象g，next(g)<=>g.send(None)
    - 3 只有当生成器出在暂停状态，才能传入非None值
    - 4 Send风阀是为协程而增加的API，所以：
        - 1 若将生成器视为协程，应只用send
        - 2 若视为迭代器，仍用next
    
    当用作迭代器时，它的生命周期取决于有多少元素可以迭代
    当做协程时，任务的终止应该可控。用close()方法结束协程
    g.close()
    或者不被显示的资源回收了，也会自动触发：
    del g
    
    如果协程代码复杂，可能需要结束时做善后处理，例如释放资源等；
    类似于StopIteration的实现机制，结束协程也是靠异常实现的
'''

'''
    使用throw()将异常抛给yield
'''
def gen_echo():
    while True:
        try:
            x = yield
        except GeneratorExit:
            print("Exit, bye")
            return
        except KeyboardInterrupt:
            print("按下了 Ctrl+C")
        else:
            print(x)

g = gen_echo()
g.send(None)
g.throw(KeyboardInterrupt)

'''
    协程的几个功能：
    - 1 在yield位置产出数据
    - 2 在yield位置暂停
    - 3 在yield位置恢复，并接收新的参数
    - 4 在yield位置传入结束信号
    - 5 在yield位置传入其他异常
    
    - 1 协程并不能消除阻塞
    - 2 协程具有传染性
    - 3 协程通过yield把阻塞换个方式传递给上游
    - 4 最终阻塞仍需要被解决
'''