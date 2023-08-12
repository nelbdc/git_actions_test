import pytest
from ..nav import fibonacci
from ..cache import fibonacci_cache, fibonacci_lru_cache
from ..conftest import time_tracker
from ..dynamic import fibonacci_dynamic, fibonacci_dynamic_more

# def get_of_list_kwargs_function(identifiers, values):
#     print(f"getting list of kwargs for function, \n{identifiers} {values}")
#     parsed_identifiers = identifiers.split(",")
#     list_of_kwargs_for_function = []
#     for tuples in values:
#         kwargs_for_function = {}
#         for i, k in enumerate(parsed_identifiers):
#             kwargs_for_function[k] = tuples[i]
#         list_of_kwargs_for_function.append(kwargs_for_function)

#     print(f"{list_of_kwargs_for_function}")
#     return list_of_kwargs_for_function


# def my_parametrized(identifiers, values):
#     def my_parametrized_function(function):
#         def func_parametrized():
#             list_of_kwargs_function = get_of_list_kwargs_function(identifiers, values)
#             for kwargs_for_function in list_of_kwargs_function:
#                 print(
#                     f"calling function {function.__name__} with {kwargs_for_function}"
#                 )
#                 function(**kwargs_for_function)

#     return my_parametrized_function


# @my_parametrized(identifiers="n,expected", values=[(0, 0), (1, 1), (2, 1), (20, 6765)])
@pytest.mark.parametrize(
    "fib_func",
    [
        fibonacci,
        fibonacci_cache,
        fibonacci_lru_cache,
        fibonacci_dynamic,
        fibonacci_dynamic_more,
    ],
)
@pytest.mark.parametrize(
    "n,expected",
    [
        (0, 0),
        (1, 1),
        (2, 1),
        (20, 6765),
    ],
)
def test_fibonacci(time_tracker, fib_func, n: int, expected: int) -> None:
    resp = fib_func(n)
    assert resp == expected
