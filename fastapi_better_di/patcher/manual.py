from inspect import Signature, signature
from typing import Callable, Optional, List

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

    get_dependant._IS_PATHED = True


def get_dependant_patched(*args, **kwargs) -> Dependant:
    kwargs = {**get_dependant.__kwdefaults__, **kwargs}
    if getattr(kwargs["call"], "_IS_PATCHED", None) is None:
        from fastapi_better_di.exceptions import EarlyInit
        from fastapi_better_di.patcher._utils import patch_endpoint_handler
        from fastapi_better_di._utils import current_app

        try:
            app = current_app.get()
        except LookupError:
            raise EarlyInit("The main app must be initialized before importing routers")

        patch_endpoint_handler(kwargs["call"], app.dependency_overrides)

    return get_dependant.__original__(*args, **kwargs)
