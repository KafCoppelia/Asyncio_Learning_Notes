
'''
    闭包和自由变量
'''
from asyncio import Task


def outer(x):
    data = {}
    def inner(value):
        data[x] = value
        
    return inner


'''
    装饰器四种形态
'''

# 一次性，仅对原函数做了额外的操作
def dec_0(f):
    # do something
    return f

# 加入配置选项，可以传递更多信息
def dec_1(*opts):
    def dec(f):
        # do something
        return f
    return dec

# 返回一个针对原函数的包装函数，每次调用时增加额外的操作，同时保留了原函数执行过程
def dec_2(f):
    def wrapper(*args, **kwargs):
        # do something
        return f(*args, **kwargs)
    return wrapper

# 1+2
def dec_3(*opts):                       # 配置函数
    def dec(f):                         # 装饰器函数
        def wrapper(*args, **kwargs):   # 包装函数
            # do something
            return f(*args, **kwargs)
        return wrapper
    return dec

'''
    什么是Callable
'''

def foo():
    pass

foo() # 针对函数的Call

class C:
    def __new__(cls, *args, **kwargs):
        print("new with:", args, kwargs)
        return super(C, cls).__new__(cls)
    
    def __init__(self, *args, **kwargs):
        print("init with:", args, kwargs)
    
    def __call__(self, *args, **kwargs):
        print("call with:", args, kwargs)
        
c = C(1,2,3) # 实例化对应的call
r = C(4,5,6) # 针对对象的call
print(r)

#####################
class Dec1:
    def __init__(self, *opts):
        self.opts = opts
        
    def __call__(self, f):
        return f
    
class Dec2:
    def __init__(self, f):
        self.f = f
        
    def __call__(self, *args, **kwargs):
        return self.f(*args, **kwargs)
    
class Dec3:
    def __init__(self, *opts):
        self.opts = opts
        
    def __call__(self, f):
        self.f = f
        return self.wrapper
        
    def wrapper(self, *args, **kwargs):
        print("warpping...", args, kwargs)
        return self.f(*args, **kwargs)
    
@Dec2
def foo():
    pass