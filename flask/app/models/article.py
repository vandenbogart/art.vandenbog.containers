from .event import Event

class Article(Event):
    "Definition of an Article record"
    title: str
    filename: str
    html: str
    created_date: str
    last_modified_date: str
    deleted: bool = False
