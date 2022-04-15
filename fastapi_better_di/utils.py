from inspect import signature
from typing import Callable, Dict

from fastapi.params import Depends


def _patch_function(func: Callable, dependencies: Dict[Callable, Callable]) -> None:
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
