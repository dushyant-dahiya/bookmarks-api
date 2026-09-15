import pytest
from fastapi.testclient import TestClient

from bookmarks_api import operations
from bookmarks_api.main import app

client = TestClient(app)


def test_create_and_list_bookmark() -> None:
    response = client.post(
        "/bookmarks",
        json={"url": "https://example.com", "title": "Example", "tags": [], "notes": ""},
    )
    assert response.status_code == 200
    created = response.json()
    assert created["title"] == "Example"

    list_response = client.get("/bookmarks")
    assert list_response.status_code == 200
    assert len(list_response.json()) >= 1


def test_created_bookmark_has_correct_id() -> None:
    response = client.post(
        "/bookmarks",
        json={"url": "https://example.com", "title": "Example", "tags": [], "notes": ""},
    )
    created = response.json()
    assert created["id"] == 1


@pytest.fixture(autouse=True)
def reset_database() -> None:
    operations.database_db.clear()
    operations.next_id = 1
