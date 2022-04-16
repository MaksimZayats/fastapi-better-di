from fastapi import APIRouter

from custom_types import MyType

api = APIRouter()


@api.get("/")
def handler(my_type: MyType):
    return {"my_type": my_type.value}
