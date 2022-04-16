import pytest
from fastapi.testclient import TestClient

from fastapi_better_di.patcher.manual import is_pathed
from tests.shared import MY_TYPE_OBJECT, get_app

app = get_app(do_patching=True, use_di_types=False)
client = TestClient(app)


def test_is_pathed():
    assert is_pathed()


@pytest.mark.parametrize(
    "url",
    (
        "di_without_depends",
        "di_with_depends_without_function_as_argument",
        "di_default_fastapi_di",
    ),
)
def test_patching(url: str):
    assert client.get(url).json() == MY_TYPE_OBJECT.value
    assert client.get("/router/" + url).json() == MY_TYPE_OBJECT.value
