import sqlalchemy
import os


class DatabaseFactory:
    """ Static class which creates and updates the database models, as well as storing a session factory
    for database connections """

    class DatabaseEngineError(Exception):
        pass

    engine = None
    session_factory = None

    @classmethod
    def create(cls) -> bool:
        from .models import Base
        from user_data import UserData

        # Create the database path if not already created
        os.makedirs(os.path.dirname(UserData.database_path), exist_ok=True)

        con_str = UserData.database_con_str + UserData.database_path

        if cls.engine is None:  # Create the engine with debug (echo) off
            cls.engine = sqlalchemy.create_engine(con_str, echo=False)

        """ Database session factory which will be used in the context manager
        to connect to the database, <expire_on_commit> must be set to False otherwise
        the session factory becomes invalid after each commit(?)
        """
        if cls.session_factory is None:
            cls.session_factory = sqlalchemy.orm.sessionmaker(bind=cls.engine, expire_on_commit=False)

        # Create or update all of the models which was created in <database_models> using <Base>
        Base.metadata.create_all(cls.engine)

        return True


class DatabaseSession:
    """ Context manager for connecting to the database """
    def __init__(self):
        if DatabaseFactory.session_factory is None or DatabaseFactory.engine is None:
            raise DatabaseFactory.DatabaseEngineError("Database session or engine has not been initialised yet")

    def __enter__(self):
        self.session = sqlalchemy.orm.scoped_session(DatabaseFactory.session_factory)

        return self.session

    def __exit__(self, *args):
        #  Auto-commit and auto-flush can be enabled when creating the factory but I prefer to see the method calls
        self.session.commit()
        self.session.flush()
        self.session.close()
