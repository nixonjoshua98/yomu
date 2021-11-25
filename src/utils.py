import threading
from typing import Any, Iterable, Optional, TypeVar
import datetime as dt

T = TypeVar("T")


def utcnow(): return dt.datetime.utcnow()


def get(ls: Iterable[T], **attrs: Any) -> Optional[T]:
    """
    Search through a iterable for an element which matches all attributes.

    :param ls: Iterable to search through
    :param attrs: Attribute values to search for
    :return: The result or None
    """

    for val in ls:
        val_dict = val.__dict__

        if all(val_dict[k] == v for k, v in attrs.items()):
            return val

    return None


def run_in_pool(func, callback):

    def _run_in_pool():
        callback(func())

    (_ := threading.Thread(target=_run_in_pool)).start()
