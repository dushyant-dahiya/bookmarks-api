from sqlalchemy.orm import Session

from bookmarks_api.db_models import BookmarkORM
from bookmarks_api.models import Bookmark, BookmarkCreate

database_db: dict[int, Bookmark] = {}
next_id = 1


def _to_bookmark(orm_obj: BookmarkORM) -> Bookmark:
    return Bookmark(
        id=orm_obj.id, url=orm_obj.url, title=orm_obj.title, tags=orm_obj.tags, notes=orm_obj.notes
    )


def create_bookmark(bookmark: BookmarkCreate, db: Session) -> Bookmark:

    new_bookmark_orm = BookmarkORM(
        url=bookmark.url,
        title=bookmark.title,
        tags=bookmark.tags,
        notes=bookmark.notes,
    )
    db.add(new_bookmark_orm)
    db.commit()
    return _to_bookmark(new_bookmark_orm)


def list_bookmarks(db: Session) -> list[Bookmark]:
    all_bookmarks = db.query(BookmarkORM).all()
    return [_to_bookmark(bookmark) for bookmark in all_bookmarks]


def get_bookmark(bookmark_id: int, db: Session) -> Bookmark | None:
    fetched_bookmark = db.query(BookmarkORM).filter(BookmarkORM.id == bookmark_id).first()
    if fetched_bookmark is None:
        return None
    return _to_bookmark(fetched_bookmark)


def delete_bookmark(bookmark_id: int, db: Session) -> Bookmark | None:
    fetched_bookmark = db.query(BookmarkORM).filter(BookmarkORM.id == bookmark_id).first()
    if fetched_bookmark is None:
        return None
    db.delete(fetched_bookmark)
    db.commit()
    return _to_bookmark(fetched_bookmark)
