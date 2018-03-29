__author__ = 'shy'
__date__ = '2018/3/29 11:05'

# Tornado的 tornado.queues 模块实现了异步生产者/消费者模式的协程：Queue、LifoQueue
# 基本操作：
# q.maxsize
# q.qsize()
# q.get(timeout=None)/get_nowait(timeout=None)
# q.put(item, timeout=None)/put_nowait(item, timeout=None)
# q.task_done()
# q.join(timeout=None) 阻塞(block)直到队列中的所有项目都处理完，返回一个Future对象，超时后会抛出 tornado.gen.TimeoutError 异常
