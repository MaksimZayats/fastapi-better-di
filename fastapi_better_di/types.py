from contextvars import ContextVar
from typing import Any, Callable, Type

from fastapi import APIRouter, FastAPI
from fastapi.routing import APIRoute

from fastapi_better_di.exeptions import EarlyInit
from fastapi_better_di.patcher._utils import patch_endpoint_handler

_current_app: ContextVar[FastAPI] = ContextVar("_current_app")


class FastAPIDI(FastAPI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__init_di__(*args, **kwargs)

    def __init_di__(self, *args, **kwargs):  # NOQA
        _current_app.set(self)

    def include_router(self, router: APIRouter, *args, **kwargs):
        self._include_router_di(router, *args, **kwargs)
        return super().include_router(router, *args, **kwargs)

    def _include_router_di(self, router: APIRouter, *args, **kwargs):
        for route in router.routes:
            patch_endpoint_handler(route.endpoint, self.dependency_overrides)


class APIRouteDI(APIRoute):
    def __init__(self, path: str, endpoint: Callable[..., Any], *args, **kwargs):
        self.__init_di__(path, endpoint, *args, **kwargs)
        super().__init__(path, endpoint, *args, **kwargs)

    def __init_di__(self, path: str, endpoint: Callable[..., Any], *args, **kwargs):  # NOQA
        try:
            current_app = _current_app.get()
        except LookupError:
            raise EarlyInit("The main app must be initialized before importing routers")

        patch_endpoint_handler(endpoint, current_app.dependency_overrides)


class APIRouterDI(APIRouter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__init_di__(*args, **kwargs)

    def __init_di__(self, *args, **kwargs):  # NOQA
        route_class: Type[APIRoute] = kwargs.get("route_class", APIRouteDI)

        if issubclass(route_class, APIRouteDI):
            self.route_class = route_class
        else:
            self.route_class = APIRouteDI
