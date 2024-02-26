from io import BytesIO

import pytest
from fastapi.testclient import TestClient

from src.main import app as app_object
from src.settings import BASE_PATH


@pytest.fixture()
def app() -> TestClient:
    return TestClient(app_object)


@pytest.fixture()
def sample_file() -> str:
    file = BASE_PATH / "images" / "sample.jpg"
    file.touch()
    yield file.name
    file.unlink()


@pytest.fixture()
def sample_image() -> bytes:
    path = BASE_PATH / "src" / "tests" / "sample.jpg"
    return path.read_bytes()


def test_getting_existing_image(app, sample_file):
    response = app.get(f"/image/{sample_file}")
    assert response.status_code == 200


def test_getting_not_existing_image(app):
    response = app.get(f"/image/iamnothere.png")
    assert response.status_code == 404


def test_submitting_incorrect_image(app):
    response = app.post("/image", files={"file": BytesIO(b"asdf")})
    assert response.status_code == 400


def test_submitting_correct_image(app, sample_image):
    response = app.post("/image", files={"file": sample_image})
    assert response.status_code == 204
