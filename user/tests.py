from django.test import TestCase


# 测试多个装饰器的装饰顺序
# 结论:多个装饰器装饰同一个函数的时候，装饰的顺序是从下到上的，执行的顺序是从上到下的
def wrapper1(func):

    def function():
        print('wrapper1已经开始执行了')
        return func()
    print('wrapper1已经装饰')
    return function


def wrapper2(func2):

    def func():
        print('wrapper2已经开始执行')
        return func2()
    print('wrapper2已经装饰')
    return func


@wrapper2
@wrapper1
def test():
    return 1 + 1


print(test())
