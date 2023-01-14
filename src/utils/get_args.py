from inspect import Parameter, signature
from typing import Callable


def get_req_arg_len(func: Callable) -> int:  # type: ignore
    params = signature(func).parameters.values()
    return len([p for p in params if type(p.default) == Parameter.empty])


def get_opt_arg_len(func: Callable) -> int:  # type: ignore
    params = signature(func).parameters.values()
    return len([p for p in params if not type(p.default) == Parameter.empty])
