# fibonacci

def fibonacci_dynamic(n):
    fib_list = [0, 1]
    for i in range(n + 1):
        fib_list.append(fib_list[i] + fib_list[i + 1])
    return fib_list[n]


def fibonacci_dynamic_more(n):
    fib_1, fib_2 = 0, 1
    for i in range(1,n + 1):
        fi = fib_1 + fib_2
        fib_1, fib_2 = fib_2, fi
    return fib_1
