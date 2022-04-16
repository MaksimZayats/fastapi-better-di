from typing import Any

from fastapi import FastAPI, Depends, APIRouter


class MyType:
    def __init__(self, value: Any):
        self.value = value


MY_TYPE_OBJECT = MyType(123)


def get_my_type() -> MyType:
    return MY_TYPE_OBJECT


def get_app(do_patching: bool, use_di_types: bool) -> FastAPI:
    if do_patching:
        from fastapi_better_di.patcher.manual import patch

        patch()

    if use_di_types:
        from fastapi_better_di import FastAPIDI, APIRouterDI

        _FastAPI = FastAPIDI
        _APIRouter = APIRouterDI
    else:
        _FastAPI = FastAPI
        _APIRouter = APIRouter

    app = _FastAPI()
    app.dependency_overrides[MyType] = get_my_type

    router = _APIRouter(prefix="/router")

    @app.get("/di_without_depends")
    @router.get("/di_without_depends")
    def di_without_depends(data: MyType):
        return data.value

    @app.get("/di_with_depends_without_function_as_argument")
    @router.get("/di_with_depends_without_function_as_argument")
    def di_with_depends_without_function_as_argument(data: MyType = Depends()):
        return data.value

    @app.get("/di_default_fastapi_di")
    @router.get("/di_default_fastapi_di")
    def di_with_depends_without_function_as_argument(
        data: MyType = Depends(get_my_type),
    ):
        return data.value

    app.include_router(router)

    return app
