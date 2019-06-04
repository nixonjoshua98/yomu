
import database.models
import database.alchemy

import functions


class InvalidFields(Exception):
    pass


""" Generic SQLAlchemy queries """


def _select_all_where_equals(table, **kwargs):
    with database.alchemy.DatabaseSession() as session:
        query = session.query(table).filter_by(**kwargs).all()
    return query


def _select_one_where_equals(table, **kwargs):
    with database.alchemy.DatabaseSession() as session:
        query = session.query(table).filter_by(**kwargs).first()
    return query


def _select_everything(table):
    with database.alchemy.DatabaseSession() as session:
        query = session.query(table).all()
    return query


def _select_all_in_list(table, field, ls):
    with database.alchemy.DatabaseSession() as session:
        query = session.query(table).filter(field.in_(ls)).all()
    return query


def _insert_row_with_values(table, need_all_fields=False, **kwargs):
    if need_all_fields and not functions.all_fields_have_value(table, kwargs.keys()):
        return False

    elif not functions.can_make_row(table, **kwargs):
        return False

    completed = False

    with database.alchemy.DatabaseSession() as session:
        row = table(**kwargs)
        session.add(row)
        completed = not completed

    return completed


def _update_row_where_equals(table, old_row_values: dict, new_row_values: dict):
    completed = False

    with database.alchemy.DatabaseSession() as session:
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

    with database.alchemy.DatabaseSession() as session:
        row = session.query(table).filter_by(**kwargs).one()

        session.delete(row)

        completed = not completed

    return completed


""" Manga table queries """


def manga_select_all_with_status(status):
    return _select_all_where_equals(database.models.Manga, status=status)


def manga_select_one_with_id(_id):
    return _select_one_where_equals(database.models.Manga, id=_id)


def manga_select_one_with_title(title):
    return _select_one_where_equals(database.models.Manga, title=title)


def manga_select_all_rows():
    return _select_everything(database.models.Manga)


def manga_select_all_in_status_list(ls):
    return _select_all_in_list(database.models.Manga, database.models.Manga.status, ls)


def manga_insert_row(**values):
    return _insert_row_with_values(database.models.Manga, need_all_fields=False, **values)


def manga_update_with_id(_id, **values):
    return _update_row_where_equals(database.models.Manga, {"id": _id}, values)


def manga_delete_with_id(_id):
    return _delete_where_equals(database.models.Manga, id=_id)
