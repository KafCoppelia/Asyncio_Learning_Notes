import collections
import random
import threading
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
    
class Future:
    def __init__(self):
        global loop
        self._loop = loop
        self._result = None
        self._done = False
        self._callbacks = []
    
    def set_result(self, result):
        if self._done:
            raise RuntimeError("Future already done")
    
        self._result = result
        self._done = True
        
        for cb in self._callbacks:
            self._loop.call_soon(cb)
    
    def result(self):
        if self._done:
            return self._result
        else:
            raise RuntimeError("Future is not done")
    
    def add_done_callback(self, callback):
        self._callbacks.append(callback)
        
    def __await__(self):
        yield self
        return self.result()

task_id = itertools.count(1)
        
class Task(Future):
    def __init__(self, coro):
        super().__init__()
        self.coro = coro
        # self._done = False
        # self._result = None
        self._id = f"Task-{next(task_id)}"
        self._loop.call_soon(self.run)
        self._start_time = time.time()
    
    def run(self):
        print(f"------{self._id}------")
        if not self._done:
            try:
                x = self.coro.send(None)
            except StopIteration as e:
                self.set_result(e.value)
                # self._result = e.value
                # self._done = True
                global total_block_time
                total_block_time += time.time() - self._start_time
            else:
                assert isinstance(x, Future)
                # 何时恢复执行？
                x.add_done_callback(self.run)
        else:
            print("Task done")
            
        print("--------------")
    
async def small_task():
    global loop
    fut = Future()
    # 指派一个目标来执行 set_result
    fake_io_read(fut)
    
    result = await fut
    return result

def fake_io_read(future):
    def read():
        time.sleep(random.random())  # IO阻塞
        future.set_result(random.randint(1, 100))
    threading.Thread(target=read).start()

def until_all_done(tasks):
    tasks = [t for t in tasks if not t._done]
    if tasks:
        loop.call_soon(until_all_done, tasks)
    else:
        loop.stop()
    

if __name__ == "__main__": 
    loop = Evenloop()
    total_block_time = 0
    start_time = time.time()
    
    all_tasks = [Task(small_task()) for i in range(2000)] # 可比较时间，观察协程如何节约时间
        
    loop.call_later(1, until_all_done, all_tasks)
    loop.run_forever()
    
    print(total_block_time, time.time() - start_time)