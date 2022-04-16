import uvicorn
from fastapi import FastAPI

from custom_types import MyType
from fastapi_better_di.patcher.auto import is_pathed

assert is_pathed(), "Something went wrong"

app = FastAPI()

app.dependency_overrides[MyType] = lambda: MyType(123)


def register_routers():
    from routes import api

    app.include_router(router=api)


register_routers()


def main():
    uvicorn.run(app=app)


if __name__ == "__main__":
    main()
