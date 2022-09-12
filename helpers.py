
import functools


def foldr(func, accumulator, arr):
    return functools.reduce(lambda x, y: func(y, x), arr[::-1], accumulator)

def foldl(func, accumulator, arr):
    return functools.reduce(lambda x, y: func(y, x), arr[1::], accumulator)
