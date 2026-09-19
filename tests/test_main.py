from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker

from bookmarks_api.database import get_db
from bookmarks_api.db_models import Base, BookmarkORM
from bookmarks_api.main import app

TEST_DATABASE_URL = (
    "postgresql://bookmarks_user:bookmarks_password@localhost:5432/bookmarks_test_db"
)

test_engine = create_engine(TEST_DATABASE_URL)
TestSessionLocal = sessionmaker(bind=test_engine)


def get_test_db() -> Iterator[Session]:
    session = TestSessionLocal()
    try:
        yield session
    finally:
        session.close()


app.dependency_overrides[get_db] = get_test_db

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
    Base.metadata.create_all(bind=test_engine)
    session = TestSessionLocal()
    session.query(BookmarkORM).delete()
    session.execute(text("ALTER SEQUENCE bookmarks_id_seq RESTART WITH 1"))
    session.commit()
    session.close()
