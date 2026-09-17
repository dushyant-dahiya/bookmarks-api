from bookmarks_api.database import SessionLocal
from bookmarks_api.db_models import BookmarkORM
from bookmarks_api.models import Bookmark, BookmarkCreate

database_db: dict[int, Bookmark] = {}
next_id = 1


def _to_bookmark(orm_obj: BookmarkORM) -> Bookmark:
    return Bookmark(
        id=orm_obj.id, url=orm_obj.url, title=orm_obj.title, tags=orm_obj.tags, notes=orm_obj.notes
    )


def create_bookmark(bookmark: BookmarkCreate) -> Bookmark:

    session = SessionLocal()
    new_bookmark_orm = BookmarkORM(
        url=bookmark.url,
        title=bookmark.title,
        tags=bookmark.tags,
        notes=bookmark.notes,
    )
    session.add(new_bookmark_orm)
    session.commit()
    return _to_bookmark(new_bookmark_orm)


def list_bookmarks() -> list[Bookmark]:
    session = SessionLocal()
    all_bookmarks = session.query(BookmarkORM).all()
    return [_to_bookmark(bookmark) for bookmark in all_bookmarks]


def get_bookmark(bookmark_id: int) -> Bookmark | None:
    session = SessionLocal()
    fetched_bookmark = session.query(BookmarkORM).filter(BookmarkORM.id == bookmark_id).first()
    if fetched_bookmark is None:
        return None
    return _to_bookmark(fetched_bookmark)


def delete_bookmark(bookmark_id: int) -> Bookmark | None:
    session = SessionLocal()
    fetched_bookmark = session.query(BookmarkORM).filter(BookmarkORM.id == bookmark_id).first()
    if fetched_bookmark is None:
        return None
    session.delete(fetched_bookmark)
    session.commit()
    return _to_bookmark(fetched_bookmark)
