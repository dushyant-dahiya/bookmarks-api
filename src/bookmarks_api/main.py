from fastapi import FastAPI, HTTPException

from bookmarks_api import operations
from bookmarks_api.models import Bookmark, BookmarkCreate

app = FastAPI()


@app.get("/bookmarks")
def list_bookmarks() -> list[Bookmark]:
    return operations.list_bookmarks()


@app.post("/bookmarks")
def create_bookmark(bookmark: BookmarkCreate) -> Bookmark:
    return operations.create_bookmark(bookmark)


@app.get("/bookmarks/{bookmark_id}")
def get_bookmark(bookmark_id: int) -> Bookmark:
    bookmark = operations.get_bookmark(bookmark_id)
    if bookmark is None:
        raise HTTPException(status_code=404, detail="Bookmark not found")
    return bookmark


@app.delete("/bookmarks/{bookmark_id}")
def delete_bookmark(bookmard_id: int) -> Bookmark:
    bookmark = operations.delete_bookmark(bookmard_id)
    if bookmark is None:
        raise HTTPException(status_code=404, detail="Bookmark not found to be deleted")
    return bookmark
