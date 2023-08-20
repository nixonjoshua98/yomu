from concurrent.futures import ThreadPoolExecutor
from typing import Any, Iterable, Optional, TypeVar, Union

T = TypeVar("T")

__thread_pool = ThreadPoolExecutor(max_workers=1)


def format_number(number: float) -> str:
    if (int_value := int(number)) == number:
        return str(int_value)
    return str(number)


def get(ls: Iterable[T], **attrs: Any) -> Optional[T]:
    for val in ls:
        val_dict = val.__dict__

        if all(val_dict[k] == v for k, v in attrs.items()):
            return val

    return None


def run_in_pool(func, callback):
    __thread_pool.submit(lambda: callback(func()))
