from inspect import signature
from typing import Callable, Dict
from typing import Optional

from fastapi.params import Depends


def patch_endpoint_handler(func: Callable, dependencies: Dict[Callable, Callable]) -> None:
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
