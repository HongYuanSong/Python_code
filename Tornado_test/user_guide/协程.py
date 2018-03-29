__author__ = 'shy'
__date__ = '2018/3/29 9:48'

from tornado import gen
from tornado.httpclient import AsyncHTTPClient
from tornado.ioloop import IOLoop

from concurrent.futures import ThreadPoolExecutor


# 通过协程机制进行异步调用
# ***tornado通过@gen.coroutine装饰器、yield生成器、Future对象实现协程***\

@gen.coroutine
def fetch_coroutine(url):
    http_client = AsyncHTTPClient()
    response = yield http_client.fetch(url)
    #  raise gen.Return(response.body)
    return response.body  # python3.3


# Python 3.5 引入了 async 和 await 关键字（原生协程），可以代替@gen.coroutine、yield

# async def fetch_coroutine(url):
#     http_client = AsyncHTTPClient()
#     response = await http_client.fetch(url)
#     return response.body


# Tornado 的协程执行者(coroutine runner)是多用途的,可以接受任何来自其他框架的awaitable对象，\
# 推荐组合了多个框架的应用使用Tornado的协程执行者来进行协程调度，\
# 使用 tornado.platform.asyncio.to_asyncio_future 适配器可以实现Tornado调度执行asyncio的协程


# tornado.gen.Runner 简化的内部循环（协程装饰器@gen.coroutine简单实现）
# step1：@gen.coroutine 装饰器从生成器接收Future对象，\
# step2：等待Future对象执行完成（非阻塞），\
# step3：解开Future对象，并把结果作为yield表达式结果传回生成器

def run(self):
    # send(x) makes the current yield return x.
    # It returns when the next yield is reached
    future = self.gen.send(self.next)

    def callback(f):
        self.next = f.result()
        self.run()

    future.add_done_callback(callback)


# 协程调用模式
# 1. 结合callback
@gen.coroutine
def call_task():
    # 注意这里没有传进来some_function.
    # 这里会被Task翻译成
    #   some_function(other_args, callback=callback)
    yield gen.Task(some_function, other_args)


# 2. 调用阻塞函数(通过ThreadPoolExecutor，返回和协程兼容的Futures)

thread_pool = ThreadPoolExecutor(4)


@gen.coroutine
def call_blocking():
    yield thread_pool.submit(blocking_func, args)


# 3. 并行调用（列表、字典中传入Future）

@gen.coroutine
def parallel_fetch(url1, url2):
    resp1, resp2 = yield [http_client.fetch(url1),
                          http_client.fetch(url2)]


@gen.coroutine
def parallel_fetch_many(urls):
    responses = yield [http_client.fetch(url) for url in urls]
    # 响应是和HTTPResponses相同顺序的列表


@gen.coroutine
def parallel_fetch_dict(urls):
    responses = yield {url: http_client.fetch(url)
                       for url in urls}


# 交叉存取（保存Future比yield Future更有用）
@gen.coroutine
def get(self):
    fetch_future = self.fetch_next_chunk()
    while True:
        chunk = yield fetch_future
        if chunk is None:
            break
        self.write(chunk)
        fetch_future = self.fetch_next_chunk()
        yield self.flush()

# 循环（循环中不能yield迭代器，需要从访问结果分离循环条件）

import motor
db = motor.MotorClient().test

@gen.coroutine
def loop_example(collection):
    cursor = db.collection.find()
    while (yield cursor.fetch_next):
        doc = cursor.next_object()


# 后台运行

@gen.coroutine
def minute_loop():
    while True:
        yield do_something()
        yield gen.sleep(60)


# Coroutines that loop forever are generally started with
# spawn_callback().
IOLoop.current().spawn_callback(minute_loop)


# 上一个循环运行每次花费60+N秒，N为do_something()花费的时间，为准确的每60秒运行，使用上面的交叉模式

@gen.coroutine
def minute_loop2():
    while True:
        nxt = gen.sleep(60)   # 开始计时.
        yield do_something()  # 计时后运行.
        yield nxt             # 等待计时结束.


if __name__ == '__main__':
    f_obj = fetch_coroutine("http://www.baidu.com")
