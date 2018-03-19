__author__ = 'shy'
__date__ = '2018/3/19 8:48'


# 方法一：__new__实现


# class Singleton:
#     _instance = None
#
#     def __new__(cls, *args, **kwargs):
#         if not cls._instance:
#             cls._instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
#         return cls._instance
#
class Singleton:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(Singleton, cls).__new__(*args, **kwargs)
        return cls._instance


class MyClass(Singleton):
    a = 1


if __name__ == '__main__':
    test1 = MyClass()
    test2 = MyClass()
    print(id(test1), id(test2))
    print(test1.a == test2.a)
    print(test1 == test2)
    print(test1 is test2)


##########################################################################################


# 方法二：装饰器实现


from functools import wraps


def singleton(cls):
    _instance = {}

    @wraps(cls)
    def check_instance(*args, **kwargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kwargs)
        return _instance[cls]
    return check_instance


@singleton
class MyClass:
    a = 1


if __name__ == '__main__':
    test1 = MyClass()
    test2 = MyClass()
    print(id(test1), id(test2))
    print(test1.a == test2.a)
    print(test1 == test2)
    print(test1 is test2)


##########################################################################################


# 方法三：metaclass实现


class Singleton(type):
    _instance = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instance:
            cls._instance[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instance[cls]


class MyClass(metaclass=Singleton):
    # __metaclass__ = Singleton
    a = 1


if __name__ == '__main__':
    test1 = MyClass()
    test2 = MyClass()
    print(id(test1), id(test2))
    print(test1.a == test2.a)
    print(test1 == test2)
    print(test1 is test2)


##########################################################################################


# Borg惯用法：保证类可以实例化多个对象（id不同），但对象共享属性、方法


class SingletonBorg(object):
    _state = {}

    def __new__(cls, *args, **kwargs):
        obj = super(SingletonBorg, cls).__new__(cls)
        obj.__dict__ = cls._state
        return obj


class MyClass1(SingletonBorg):
    pass


class MyClass2(SingletonBorg):
    pass


class MyClass3(SingletonBorg):
    _state = {}


if __name__ == '__main__':
    test1 = MyClass1()
    test1.a = 1
    test2 = MyClass1()
    test2.a = 2
    print(id(test1), id(test2))
    print(test1.a, test2.a)

    test11 = MyClass2()
    print(test11.a) # MyClass1、MyClass2会共享属性、方法
    test11.a = 1
    test22 = MyClass2()
    test22.a = 2
    print(id(test11), id(test22))
    print(test11.a, test22.a)

    test111 = MyClass3()
    # 执行print会报错，MyClass3重写了_state,不会跟其他子类共享属性方法，只有MyClass3内的实例对象共享属性方法
    # print(test111.a)
    test111.a = 1
    test222 = MyClass2()
    test222.a = 2
    print(id(test11), id(test22))
    print(test11.a, test22.a)

