from .database_models import Manga
from .database_alchemy import DatabaseSession

from .database_functions import (
    all_fields_have_value,
    can_make_row,
)

from .database_functions import (
    get_non_pk_fields
)


class InvalidFields(Exception):
    pass


def manga_select_with_status(status):
    with DatabaseSession() as session:
        query = session.query(Manga).filter_by(status=status).all()
    return query


def manga_select_with_id(_id):
    with DatabaseSession() as session:
        query = session.query(Manga).get(_id)
    return query


def manga_insert_row(**values):
    # Checks
    if not all_fields_have_value(Manga, values.keys()):
        return False

    if not can_make_row(Manga, **values):
        return False

    with DatabaseSession() as session:
        row = Manga(**values)
        session.add(row)

    return True


def manga_select_with_statuses(status_list):
    with DatabaseSession() as session:
        query = session.query(Manga).filter(Manga.status.in_(status_list)).all()
    return query


def manga_select_all_rows():
    with DatabaseSession() as session:
        query = session.query(Manga).all()
    return query


def manga_delete_by_id(_id):
    row = manga_select_with_id(_id)

    if row is None:
        print(f"ID {_id} cannot be deleted as it is not present in the table")
        return False

    with DatabaseSession() as session:
        session.delete(row)


def manga_update_with_id(_id, **values):
    with DatabaseSession() as session:
        row = session.query(Manga).get(_id)

        if row is None:
            print(f"ID {_id} cannot be selected as it it is not present in the table");
            return False

        for k in get_non_pk_fields(Manga):
            if values.get(k, None) is not None:
                setattr(row, k, values[k])

    return True

