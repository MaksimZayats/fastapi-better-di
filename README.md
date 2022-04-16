# fastapi-better-di

## What is this ?
`fastapi-better-di` is a utility that allows you to use DI in fastapi without Depends()

## Installation

```shell
pip install fastapi_better_di
```

## Examples

1.

```python
# routes.py
from fastapi import APIRouter

from custom_types import MyType

api = APIRouter()


@api.get("/")
def handler(my_type: MyType):  # <- DI without Depends()
    return {"my_type": my_type.value}
```

```python
# app.py
from fastapi import FastAPI
from fastapi_better_di.patcher.auto import is_pathed

from custom_types import MyType

assert is_pathed(), "Something went wrong"

app = FastAPI()

# Register types for DI
app.dependency_overrides[MyType] = lambda: MyType(123)


def register_routers():
    # Importing routers after initializing main app
    from routes import api

    app.include_router(router=api)


register_routers()
```

2. [See full examples](examples)

## Usage

You have 2 use cases:

1. Use patching:
    * Auto patching: patches classes when importing:
      ```python
      from fastapi_better_di.patcher.auto import is_pathed # The classes were patched immediately after import

      # To check if everything is OK, use assert
      assert is_pathed(), "Something went wrong"
      ```

    * Manual patching: you need to call `patch()` by yourself:
      ```python
      from fastapi_better_di.patcher.manual import patch, is_pathed

      patch()
      
      # To check if everything is OK, use assert
      assert is_pathed(), "Something went wrong"
      ```

    * [Patching example](examples/patching)
2. Use DI Classes: `FastAPIDI, APIRouterDI, APIRouteDI`
    * Use `FastAPIDI` instead of `FastAPI`
    * Use `APIRouterDI` instead of `APIRouter`
    * Use `APIRouteDI` instead of `APIRoute`
    * [DI Classes example](examples/simple)

* **IMPORTANT**: You can still use `= Depends()` without a function as an argument,
  and it won't add unnecessary arguments to the swagger.
  * Related issue: [fastapi issue](https://github.com/tiangolo/fastapi/issues/4118)

* **IMPORTANT**: The main app(`FastAPI`) and `dependency_overrides` must be initialized before importing routers!

## How it works

`fastapi-better-di` simply patch the handler function and add `= Depends(func)` as the default argument

