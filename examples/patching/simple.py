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
