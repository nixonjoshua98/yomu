import sqlalchemy

from .factory import DatabaseFactory


class DatabaseSession:
    """ Context manager for connecting to the database """

    def __enter__(self):
        self.session = sqlalchemy.orm.scoped_session(DatabaseFactory.session_factory)

        return self.session

    def __exit__(self, *args):
        self.session.commit()
        self.session.flush()
        self.session.close()
