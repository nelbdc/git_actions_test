from functools import lru_cache

cache = {}


def fibonacci_cache(n):
    if n in cache:
        return cache[n]
    if n < 2:
        return n

    fn = fibonacci_cache(n - 2) + fibonacci_cache(n - 1)
    cache[n] = fn
    return fn


@lru_cache(maxsize=256)
def fibonacci_lru_cache(n):
    if n < 2:
        return n
    return fibonacci_cache(n - 2) + fibonacci_cache(n - 1)
