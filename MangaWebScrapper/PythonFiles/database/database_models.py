import sqlalchemy.ext.declarative

from sqlalchemy import (
    Column,
    Integer,
    String,
    Sequence,
    Float,
    Boolean
    )

Base = sqlalchemy.ext.declarative.declarative_base()


class Manga(Base):
    __tablename__ = "manga"

    # Auto-increment primary key
    id = Column(Integer, Sequence("user_id_seq"), primary_key=True)
    title = Column(String(256))
    menu_url = Column(String(256))
    chapters_read = Column(Float)
    status = Column(Integer)
    hidden = Column(Boolean)

    def __str__(self):
        return f"({self.id}, {self.title}, {self.menu_url}, {self.chapters_read}, {self.status}, {self.hidden})"
