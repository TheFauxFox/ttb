from inspect import signature
from typing import Callable


def get_arg_len(func: Callable) -> int:  # type: ignore
    return len(signature(func).parameters)
