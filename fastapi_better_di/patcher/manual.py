from inspect import Signature, signature

from fastapi import FastAPI
from fastapi.dependencies.models import Dependant
from fastapi.dependencies.utils import get_dependant

from fastapi_better_di._utils import current_app
from fastapi_better_di.patcher._utils import copy_func, decorate_method


def is_pathed() -> bool:
    return all(
        (
            getattr(FastAPI.__init__, "_IS_PATHED", False),
            getattr(get_dependant, "_IS_PATHED", False),
        )
    )


def patch():
    FastAPI.__init__ = decorate_method(
        FastAPI.__init__, after_call=lambda self, *_, **__: current_app.set(self)
    )

    get_dependant.__original__ = copy_func(get_dependant)
    get_dependant.__code__ = get_dependant_patched.__code__
    get_dependant.__signature__ = signature(get_dependant.__original__)
    get_dependant.__cache__ = {}

    get_dependant._IS_PATHED = True


def get_dependant_patched(*args, **kwargs) -> Dependant:
    cache_key = hash(kwargs["call"])

    if cache_key in get_dependant.__cache__:  # type: ignore
        return get_dependant.__cache__[cache_key]  # type: ignore

    from fastapi_better_di.exeptions import EarlyInit
    from fastapi_better_di.patcher._utils import patch_endpoint_handler
    from fastapi_better_di._utils import current_app

    get_dependant_original = get_dependant.__original__  # type: ignore

    sig: Signature = get_dependant_original.__signature__

    default_args = {
        k: v.default for k, v in sig.parameters.items() if v.default is not sig.empty
    }

    kwargs = {**default_args, **kwargs}

    try:
        app = current_app.get()
    except LookupError:
        raise EarlyInit("The main app must be initialized before importing routers")

    patch_endpoint_handler(kwargs["call"], app.dependency_overrides)
    result = get_dependant_original(*args, **kwargs)

    get_dependant.__cache__[cache_key] = result  # type: ignore

    return result
