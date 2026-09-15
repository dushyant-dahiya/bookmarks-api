from fastapi import FastAPI

from bookmarks_api import operations
from bookmarks_api.models import Bookmark, BookmarkCreate

app = FastAPI()


@app.get("/bookmarks")
def list_bookmarks() -> list[Bookmark]:
    return operations.list_bookmarks()


@app.post("/bookmarks")
def create_bookmark(bookmark: BookmarkCreate) -> Bookmark:
    return operations.create_bookmark(bookmark)
