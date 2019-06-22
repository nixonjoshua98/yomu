import os
import sqlalchemy

from user_data import UserData


class DatabaseFactory:
	engine, session_factory = None, None

	@classmethod
	def create_engine(cls):
		from .models import Base

		# Create the database path if not already created
		os.makedirs(os.path.dirname(UserData.database_path), exist_ok=True)

		con_str = UserData.database_con_str + UserData.database_path

		cls.engine = sqlalchemy.create_engine(con_str, echo=False)

		Base.metadata.create_all(cls.engine)

	@classmethod
	def create_factory(cls):
		if cls.engine is None:
			raise ValueError("Engine cannot be None when creating database session factory")

		""" Database session factory which will be used in the context manager
		to connect to the database, <expire_on_commit> must be set to False otherwise
		the session factory becomes invalid after each commit(?)
		"""
		cls.session_factory = sqlalchemy.orm.sessionmaker(bind=cls.engine, expire_on_commit=False)