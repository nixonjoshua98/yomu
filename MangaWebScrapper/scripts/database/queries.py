
from . import models
from . import DatabaseSession

from scripts import data


def select_all_manga():
	with DatabaseSession() as session:
		query = session.query(models.Manga).all()
	return query


def select_all_downloadable_manga():
	status_keys = data.manga_status.get_all_downloadable(keys_only=True)

	with DatabaseSession() as session:
		query = session.query(models.Manga).filter(models.Manga.status.in_(status_keys)).all()
	return query
