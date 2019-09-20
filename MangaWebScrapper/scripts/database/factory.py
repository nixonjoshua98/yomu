import os
import sqlalchemy
import sqlalchemy.orm

import scripts.data as data


class DatabaseFactory:
	engine, session_factory = None, None

	@classmethod
	def create(cls):
		from .models import Base

		os.makedirs(os.path.dirname(data.paths.DATABASE_PATH), exist_ok=True)

		con_str = f"sqlite:///{data.paths.DATABASE_PATH}"

		cls.engine = sqlalchemy.create_engine(con_str, echo=False)

		if cls.engine is None:
			raise ValueError("Engine cannot be None when creating database session factory")

		Base.metadata.create_all(cls.engine)  # Create the models

		""" Database session factory which will be used in the context manager
		to connect to the database, <expire_on_commit> must be set to False otherwise
		the session factory becomes invalid after each commit(?)
		"""

		cls.session_factory = sqlalchemy.orm.sessionmaker(bind=cls.engine, expire_on_commit=False)