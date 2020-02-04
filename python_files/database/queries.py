
import functions

from python_files.database.context_manager import DatabaseSession
from python_files.database import models
from python_files.common import manga_status


class InvalidFields(Exception):
    pass


def get_all_downloadable():
    with DatabaseSession() as session:
        s = session.query(models.Manga)

        query = s.filter(models.Manga.status.in_(manga_status.all_downloadable_ids()))

        # query = s.filter(models.Manga.status.in_((0, )))

        results = query.all()

    return results


def update_latest_chapter(*, _id: int, chapter: int):
    with DatabaseSession() as session:
        row = session.query(models.Manga).filter_by(id=_id).first()

        row.latest_chapter = chapter


def _select_all_where_equals(table, **kwargs):
    with DatabaseSession() as session:
        query = session.query(table).filter_by(**kwargs).all()
    return query


def _select_one_where_equals(table, **kwargs):
    with DatabaseSession() as session:
        query = session.query(table).filter_by(**kwargs).first()
    return query


def _select_everything(table):
    with DatabaseSession() as session:
        query = session.query(table).all()
    return query


def _select_all_in_list(table, field, ls):
    with DatabaseSession() as session:
        query = session.query(table).filter(field.in_(ls)).all()
    return query


def _insert_row_with_values(table, need_all_fields=False, **kwargs):
    if need_all_fields and not functions.all_fields_have_value(table, kwargs.keys()):
        return False

    elif not functions.can_make_row(table, **kwargs):
        return False

    completed = False

    with DatabaseSession() as session:
        row = table(**kwargs)
        session.add(row)
        completed = not completed

    return completed


def _update_row_where_equals(table, old_row_values: dict, new_row_values: dict):
    completed = False

    with DatabaseSession() as session:
        row = session.query(table).filter_by(**old_row_values).first()

        if row is not None:
            # Could be put into a map operation
            for k in functions.get_non_pk_fields(table):
                # If a new value is present
                if new_row_values.get(k, None) is not None:
                    setattr(row, k, new_row_values[k])

            completed = True

    return completed


def _delete_where_equals(table, **kwargs):
    completed = False

    with DatabaseSession() as session:
        row = session.query(table).filter_by(**kwargs).one()

        session.delete(row)

        completed = not completed

    return completed


""" Manga table queries """


def manga_select_all_with_status(status):
    return _select_all_where_equals(models.Manga, status=status)


def manga_select_one_with_id(_id):
    return _select_one_where_equals(models.Manga, id=_id)


def manga_select_one_with_title(title):
    return _select_one_where_equals(models.Manga, title=title)


def manga_select_all_rows():
    return _select_everything(models.Manga)


def manga_select_all_in_status_list(ls):
    return _select_all_in_list(models.Manga, models.Manga.status, ls)


def manga_insert_row(**values):
    return _insert_row_with_values(models.Manga, need_all_fields=False, **values)


def manga_update_with_id(_id, **values):
    return _update_row_where_equals(models.Manga, {"id": _id}, values)


def manga_delete_with_id(_id):
    return _delete_where_equals(models.Manga, id=_id)
