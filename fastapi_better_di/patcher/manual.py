from fastapi import FastAPI
from fastapi.routing import APIRoute, APIRouter

from fastapi_better_di.patcher._utils import decorate_method
from fastapi_better_di.types import FastAPIDI, APIRouteDI, APIRouterDI


def is_pathed() -> bool:
    return all((
        getattr(FastAPI.__init__, "_IS_PATHED", False),
        getattr(APIRoute.__init__, "_IS_PATHED", False),
        getattr(APIRouter.__init__, "_IS_PATHED", False),
        getattr(FastAPI.include_router, "_IS_PATHED", False),
    ))


def patch():
    FastAPI.__init__ = decorate_method(FastAPI.__init__, after_call=FastAPIDI.__init_di__)
    APIRoute.__init__ = decorate_method(APIRoute.__init__, after_call=APIRouteDI.__init_di__)
    APIRouter.__init__ = decorate_method(APIRouter.__init__, after_call=APIRouterDI.__init_di__)

    FastAPI.include_router = decorate_method(
        FastAPI.include_router,
        before_call=FastAPIDI._include_router_di  # NOQA
    )
