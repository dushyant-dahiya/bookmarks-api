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


def test_get_bookmark_success() -> None:
    create_response = client.post(
        "/bookmarks",
        json={"url": "https://example.com", "title": "Example", "tags": [], "notes": ""},
    )

    created = create_response.json()
    bookmark_id = created["id"]

    get_response = client.get(
        f"/bookmarks/{bookmark_id}",
    )
    assert get_response.status_code == 200
    fetched = get_response.json()
    assert fetched["id"] == bookmark_id
    assert fetched["title"] == "Example"


def test_get_bookmark_not_exist() -> None:
    create_reponse = client.post(
        "/bookmarks",
        json={"url": "https://example.com", "title": "Example", "tags": [], "notes": ""},
    )
    assert create_reponse.status_code == 200
    created = create_reponse.json()
    assert created["id"] == 1

    bookmark_id = 999
    get_response = client.get(f"/bookmarks/{bookmark_id}")
    assert get_response.status_code == 404


def test_delete_bookmark_success() -> None:

    create_response = client.post(
        "/bookmarks",
        json={"url": "https://example.com", "title": "Example", "tags": [], "notes": ""},
    )

    assert create_response.status_code == 200
    created = create_response.json()
    bookmark_id = created["id"]

    delete_response = client.delete(f"/bookmarks/{bookmark_id}")
    deleted = delete_response.json()

    assert deleted["id"] == bookmark_id
    assert deleted["title"] == "Example"

    verify_response = client.get(f"/bookmarks/{bookmark_id}")
    assert verify_response.status_code == 404


def test_delete_bookmark_not_exist() -> None:
    create_reponse = client.post(
        "/bookmarks",
        json={"url": "https://example.com", "title": "Example", "tags": [], "notes": ""},
    )
    assert create_reponse.status_code == 200
    created = create_reponse.json()
    assert created["id"] == 1

    bookmark_id = 999
    delete_response = client.delete(f"/bookmarks/{bookmark_id}")
    assert delete_response.status_code == 404


@pytest.fixture(autouse=True)
def reset_database() -> None:
    operations.database_db.clear()
    operations.next_id = 1
