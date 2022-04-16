from custom_types import MyType

from fastapi_better_di import APIRouterDI

api = APIRouterDI()


@api.get("/")
def handler(my_type: MyType):
    return {"my_type": my_type.value}
