from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from bookmarks_api import operations
from bookmarks_api.database import engine, get_db
from bookmarks_api.db_models import Base
from bookmarks_api.models import Bookmark, BookmarkCreate

app = FastAPI()

Base.metadata.create_all(engine)


@app.get("/bookmarks")
def list_bookmarks(db: Session = Depends(get_db)) -> list[Bookmark]:  # noqa: B008
    return operations.list_bookmarks(db)


@app.post("/bookmarks")
def create_bookmark(bookmark: BookmarkCreate, db: Session = Depends(get_db)) -> Bookmark:  # noqa: B008
    return operations.create_bookmark(bookmark, db)


@app.get("/bookmarks/{bookmark_id}")
def get_bookmark(bookmark_id: int, db: Session = Depends(get_db)) -> Bookmark:  # noqa: B008
    bookmark = operations.get_bookmark(bookmark_id, db)
    if bookmark is None:
        raise HTTPException(status_code=404, detail="Bookmark not found")
    return bookmark


@app.delete("/bookmarks/{bookmark_id}")
def delete_bookmark(bookmark_id: int, db: Session = Depends(get_db)) -> Bookmark:  # noqa: B008
    bookmark = operations.delete_bookmark(bookmark_id, db)
    if bookmark is None:
        raise HTTPException(status_code=404, detail="Bookmark not found to be deleted")
    return bookmark
