import os
import sqlalchemy

from python_files.common import constants


class DatabaseFactory:
	engine, session_factory = None, None

	@classmethod
	def create_engine(cls):
		from .models import Base

		# Create the database path if not already created
		os.makedirs(os.path.dirname(constants.DB_FILE), exist_ok=True)

		cls.engine = sqlalchemy.create_engine(f"sqlite:///{constants.DB_FILE}", echo=False)

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