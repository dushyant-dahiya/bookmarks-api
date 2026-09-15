from bookmarks_api.models import Bookmark, BookmarkCreate

database_db: dict[int, Bookmark] = {}
next_id = 1


def create_bookmark(bookmark: BookmarkCreate) -> Bookmark:
    global next_id
    new_bookmark = Bookmark(
        id=next_id, url=bookmark.url, title=bookmark.title, tags=bookmark.tags, notes=bookmark.notes
    )
    database_db[next_id] = new_bookmark
    next_id += 1

    return new_bookmark


def list_bookmarks() -> list[Bookmark]:
    bookmarks = []
    for bookmark in database_db.values():
        bookmarks.append(bookmark)
    return bookmarks


def get_bookmark(bookmark_id: int) -> Bookmark | None:
    bookmark = database_db.get(bookmark_id)
    if bookmark is not None:
        return bookmark
    else:
        return None
