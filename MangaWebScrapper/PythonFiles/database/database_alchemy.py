import os
import sqlalchemy

from .database_constants import *


class Database:
    engine = None
    session_factory = None

    @classmethod
    def create(cls):
        from .database_models import ( Base )

        os.makedirs(os.path.dirname(DB_PATH), exist_ok = True)

        if not cls.engine:
            cls.engine = sqlalchemy.create_engine(CON_STR + DB_PATH, echo = False)

        if not cls.session_factory:
            cls.session_factory = sqlalchemy.orm.sessionmaker(
                bind = cls.engine, 
                expire_on_commit = False,
                )

        Base.metadata.create_all(cls.engine)


class DatabaseSession:
    def __enter__(self):
        self.session = sqlalchemy.orm.scoped_session(Database.session_factory)

        return self.session

    def __exit__(self, typ, value, traceback):       
        self.session.commit()
        self.session.flush()
        self.session.close()
