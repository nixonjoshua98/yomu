import sqlalchemy.ext.declarative

from sqlalchemy import (
    Column,
    Integer,
    String,
    Sequence,
    Float,
    )

Base = sqlalchemy.ext.declarative.declarative_base()


class Manga(Base):
    __tablename__ = "manga"

    # Auto-increment primary key
    id = Column(Integer, Sequence("user_id_seq"), primary_key=True)
    title = Column(String(256))
    url = Column(String(256))
    latest_chapter = Column(Float, default=0.0)
    chapters_read = Column(Float, default=0.0)
    status = Column(Integer, default=0)

    def __str__(self):
        return f"({self.id}, {self.title}, {self.url}, {self.chapters_read}, {self.status})"
