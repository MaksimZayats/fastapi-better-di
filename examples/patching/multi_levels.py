import uvicorn
from fastapi import FastAPI

from fastapi_better_di.patcher.auto import is_pathed

# functions were patched immediately after import


assert is_pathed(), "Something went wrong"


class A:
    def __init__(self, value):
        self.value = value


class B:
    def __init__(self, value):
        self.value = value


def get_a() -> A:
    return A(3)


def get_b(a: A) -> B:  # <- multi level DI without `Depends()`
    return B(a.value ** 2)


app = FastAPI()
app.dependency_overrides[A] = get_a
app.dependency_overrides[B] = get_b


@app.get("/")
def handler(b: B):  # <- DI without `Depends()`
    assert b.value == 9
    return b


if __name__ == "__main__":
    uvicorn.run(app)
