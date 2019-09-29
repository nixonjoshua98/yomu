import os
import sqlalchemy
import sqlalchemy.orm

import scripts.data as data


class DatabaseFactory:
	session_factory = None

	@classmethod
	def create(cls):
		from .models import Base

		os.makedirs(os.path.dirname(data.paths.DATABASE_PATH), exist_ok=True)

		con_str = f"sqlite:///{data.paths.DATABASE_PATH}"

		engine = sqlalchemy.create_engine(con_str, echo=False)

		Base.metadata.create_all(engine)  # Create the models

		""" Database session factory which will be used in the context manager
		to connect to the database, <expire_on_commit> must be set to False otherwise
		the session factory becomes invalid after each commit(?)
		"""

		cls.session_factory = sqlalchemy.orm.sessionmaker(bind=engine, expire_on_commit=False)
