from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Story(Base):
    __tablename__ = "stories"

    id = Column(Integer, primary_key=True)

    title = Column(String, nullable=False)

    url = Column(String, nullable=False)

    latest_chapter = Column(Integer, nullable=False, default=0)

    latest_chapter_read = Column(Integer, nullable=False, default=0)

    status = Column(Integer, nullable=False, default=0)

    def __init__(self, title: str, url: str):
        self.title = title
        self.url = url

    def update(self, story: "Story"):
        assert self.id == story.id

        self.title = story.title
        self.url = story.url
        self.latest_chapter = story.latest_chapter
        self.latest_chapter_read = story.latest_chapter_read
        self.status = story.status
