from inspect import signature
from types import FunctionType
from typing import Callable, Dict, Optional

from fastapi.params import Depends


def patch_endpoint_handler(
    func: Callable, dependencies: Dict[Callable, Callable]
) -> None:
    if getattr(func, "_IS_PATCHED", None) is not None:
        return

    sig = signature(func)

    for parameter in sig.parameters.values():
        if parameter.annotation in dependencies:
            if isinstance(parameter.default, Depends):
                if parameter.default.dependency is not None:
                    return
                # def func(param: Type = Depends())
                dependency = dependencies[parameter.annotation]
                parameter._default.dependency = dependency  # NOQA
            elif parameter.default == parameter.empty:
                # def func(param: Type)
                dependency = dependencies[parameter.annotation]
                parameter._default = Depends(dependency)  # NOQA

    func.__signature__ = sig
    func._IS_PATCHED = True


def decorate_method(
    method: Callable,
    before_call: Optional[Callable] = None,
    after_call: Optional[Callable] = None,
) -> Callable:
    def wrapper(*args, **kwargs):
        if before_call is not None:
            before_call(*args, **kwargs)

        result = method(*args, **kwargs)

        if after_call is not None:
            after_call(*args, **kwargs)

        return result

    wrapper._IS_PATHED = True

    return wrapper


def copy_func(f, name=None) -> FunctionType:
    fn = FunctionType(
        f.__code__, f.__globals__, name or f.__name__, f.__defaults__, f.__closure__
    )

    fn.__signature__ = signature(f)
    fn.__dict__.update(f.__dict__)

    return fn
