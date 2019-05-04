import enum

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import (
    Column,
    Integer,
    String,
    Sequence,
    Enum,
    Float,
    )

Base = declarative_base()


class MangaStatusEnum(enum.Enum):
    RECENTLY_ADDED = 0
    FAVOURITES = 1
    READING_LIST = 2
    RARELY_UPDATES = 3
    DROPPED = 4
    COMPLETED = 5


class Manga(Base):
    __tablename__ = "manga"

    id = Column(Integer, Sequence("user_id_seq"), primary_key=True)
    title = Column(String(256))
    menu_url = Column(String(256))
    chapters_read = Column(Float)
    status = Column(Enum(MangaStatusEnum, name="status"))

    def __str__(self):
        return f"{self.id}, {self.title}, {self.menu_url}, {self.chapters_read}, {self.status}"
