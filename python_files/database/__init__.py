from .context_manager import DatabaseSession


def init():
	from python_files.database.factory import DatabaseFactory

	DatabaseFactory.create_engine()
	DatabaseFactory.create_factory()
