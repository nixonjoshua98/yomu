from concurrent.futures import ThreadPoolExecutor
from typing import TypeVar

T = TypeVar("T")

__thread_pool = ThreadPoolExecutor(max_workers=1)


def format_number(number: float) -> str:
    if (int_value := int(number)) == number:
        return str(int_value)
    return str(number)


def run_in_pool(func, callback):
    __thread_pool.submit(lambda: callback(func()))
