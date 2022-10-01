
import functools


def foldr(func, accumulator, arr):
    return functools.reduce(lambda x, y: func(y, x), arr[::-1], accumulator)

def foldl(func, accumulator, arr):
    return functools.reduce(lambda x, y: func(y, x), arr[1::], accumulator)

if __name__ == '__main__':
    def divide(bottom, top): return top / bottom
    test = foldr(divide, 10, [2,2])
    print(test)