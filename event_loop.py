import collections
from random import random
import time
import heapq
import itertools

class Evenloop:
    def __init__(self) -> None:
        self._ready = collections.deque()
        self._scheduled = []
        self._stopping = False
        
    def call_soon(self, callback, *args):
        self._ready.append((callback, args))
    
    def call_later(self, delay, callback, *args): 
        t = time.time() + delay
        heapq.heappush(self._scheduled, (t, callback, args))
    
    def stop(self):
        self._stopping = True
    
    def run_forever(self):
        while True:
            self.run_once()
            if self._stopping:
                break
    
    def run_once(self):
        now = time.time()
        if self._scheduled:
            if self._scheduled[0][0] < now:
                _, cb, args = heapq.heappop(self._scheduled)
                self._ready.append((cb, args))
                
        num = len(self._ready)
        for i in range(num):
            cb, args = self._ready.popleft()
            cb(*args)
    
class Awaitable:
    def __init__(self, obj) -> None:
        self.value = obj
        
    def __await__(self):
        yield self
    
    
loop = Evenloop()
task_id = itertools.count(1)
        
class Task:
    def __init__(self, coro) -> None:
        self.coro = coro
        self._done = False
        self._result = None
        self._id = f"Task-{next(task_id)}"
    
    def run(self):
        print(f"------{self._id}------")
        if not self._done:
            try:
                x = self.coro.send(None)
            except StopIteration as e:
                self._result = e.value
                self._done = True
            else:
                assert isinstance(x, Awaitable)
                loop.call_later(x.value, self.run)
        else:
            print("Task done")
            
        print("--------------")
    
async def small_task():
    t1 = time.time()
    sleep = random()
    await Awaitable(sleep) 

if __name__ == "__main__": 
    for i in range(10):
        t = Task(small_task())
        loop.call_soon(t.run)
        
    loop.call_later(3, loop.stop)
    loop.run_forever()