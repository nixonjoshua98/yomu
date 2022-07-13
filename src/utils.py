import threading
from typing import Any, Iterable, Optional, TypeVar

T = TypeVar("T")


def get(ls: Iterable[T], **attrs: Any) -> Optional[T]:
    for val in ls:
        val_dict = val.__dict__

        if all(val_dict[k] == v for k, v in attrs.items()):
            return val

    return None


def run_in_pool(func, callback):
    threading.Thread(target=lambda: callback(func())).start()
