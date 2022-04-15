# fastapi-better-di

## Installation

```shell
pip install fastapi_better_di
```

## Usage

1.
```python
# routes.py
from fastapi_better_di import APIRouterDI

from custom_types import MyType

api = APIRouterDI()

@api.get("/")
def handler(my_type: MyType):  # <- DI without Depends()
    return {"my_type": my_type.value}
```

```python
# app.py
from fastapi_better_di import FastAPIDI

from custom_types import MyType

app = FastAPIDI()

# Register types for DI
app.dependency_overrides[MyType] = lambda: MyType(123)

def register_routers():
    from routes import api

    app.include_router(router=api)

register_routers()
```

2. [See examples](examples/simple)


## How it works

`fastapi-better-di` simply patch the handler function and add `= Depends(func)` as the default argument
