from pydantic import BaseModel


class BookmarkCreate(BaseModel):
    url: str
    title: str
    tags: list[str] = []
    notes: str = ""


class Bookmark(BookmarkCreate):
    id: int
