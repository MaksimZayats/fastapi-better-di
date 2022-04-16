import pytest
from fastapi.testclient import TestClient

from tests.shared import MY_TYPE_OBJECT, get_app

app = get_app(do_patching=False, use_di_types=True)
client = TestClient(app)


@pytest.mark.parametrize(
    "url",
    (
        "di_without_depends",
        "di_with_depends_without_function_as_argument",
        "di_default_fastapi_di",
    ),
)
def test_types(url: str):
    # TODO: assert client.get(url).json() == MY_TYPE_OBJECT.value
    assert client.get("/router/" + url).json() == MY_TYPE_OBJECT.value
