from .context_manager import DatabaseSession

from .queries import *


def create():
	from .factory import DatabaseFactory

	DatabaseFactory.create()