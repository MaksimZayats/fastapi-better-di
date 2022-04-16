# Currently not working with app handlers like @app.get etc.

import uvicorn
from custom_types import MyType

from fastapi_better_di import FastAPIDI

app = FastAPIDI()

app.dependency_overrides[MyType] = lambda: MyType(123)


def register_routers():
    from routes import api

    app.include_router(router=api)


register_routers()


def main():
    uvicorn.run(app=app)


if __name__ == "__main__":
    main()
