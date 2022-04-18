# fastapi-better-di

## What is this ?
`fastapi-better-di` is a utility that allows you to use DI in fastapi without Depends()

## Installation

```shell
pip install fastapi_better_di
```

## Examples

```python
# app.py
import uvicorn
from fastapi import FastAPI
from fastapi_better_di.patcher.auto import is_pathed
# functions were patched immediately after import

assert is_pathed(), "Something went wrong"


class MyType:
    def __init__(self, value):
        self.value = value


app = FastAPI()
app.dependency_overrides[MyType] = lambda: MyType(123)


@app.get("/")
def handler(my_type: MyType):  # <- DI without `Depends()`
    assert my_type.value == 123
    return my_type


if __name__ == "__main__":
    uvicorn.run(app)
```

[See all examples](examples)

## Usage

1. Patching:
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

    * [Examples](examples)


* **IMPORTANT**: You can still use `= Depends()` without a function as an argument,
  and it won't add unnecessary arguments to the swagger.
  * Related issue: [fastapi issue](https://github.com/tiangolo/fastapi/issues/4118)

* **IMPORTANT**: The main app(`FastAPI`) and `dependency_overrides` must be initialized before importing routers!

## How it works

`fastapi-better-di` simply patch the handler function and add `= Depends(func)` as the default argument
