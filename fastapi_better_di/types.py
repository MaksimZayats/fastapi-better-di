from contextvars import ContextVar
from typing import Any, Callable, Type

from fastapi import APIRouter, FastAPI
from fastapi.routing import APIRoute

from fastapi_better_di.exeptions import EarlyInit
from fastapi_better_di.utils import _patch_function

_current_app: ContextVar[FastAPI] = ContextVar("_current_app")


class FastAPIDI(FastAPI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _current_app.set(self)

    def include_router(self, router: APIRouter, *args, **kwargs):
        for route in router.routes:
            _patch_function(route.endpoint, self.dependency_overrides)

        return super().include_router(router, *args, **kwargs)


class APIRouteDI(APIRoute):
    def __init__(self, path: str, endpoint: Callable[..., Any], *args, **kwargs):
        try:
            current_app = _current_app.get()
        except LookupError:
            raise EarlyInit("The main app must be initialized before importing routers")

        _patch_function(endpoint, current_app.dependency_overrides)
        super().__init__(path, endpoint, *args, **kwargs)


class APIRouterDI(APIRouter):
    def __init__(self, *args, route_class: Type[APIRouteDI] = APIRouteDI, **kwargs):
        super().__init__(*args, route_class=route_class, **kwargs)
