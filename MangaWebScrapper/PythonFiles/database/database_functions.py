from sqlalchemy.inspection import inspect


def get_table_fields(table) -> list:
    return table.__table__.columns.keys()


def get_table_pk(tbl) -> str:
    return inspect(tbl).primary_key[0].name


def get_table_primary_key(table):
    return inspect(table).primary_key[0].name


def get_non_pk_fields(table) -> list:
    table_fields = get_table_fields(table)
    pk = get_table_pk(table)
    table_fields.remove(pk)
    return table_fields


def remove_nasty_chars(s):
    try:
        return "".join([i for i in s if i not in ':\\/|*"><?.,'])
    except TypeError:
        return s


def all_fields_have_value(table, fields_given, ignore_pk=True):
    if ignore_pk:  # Don't check if the primary key has been given a value (normally because it auto-increments)
        table_fields = get_non_pk_fields(table)
    else:
        table_fields = table.__table__.columns.keys()

    # All fields have been given a value
    if all(map(lambda f: f in fields_given, table_fields)):
        return True
    else:
        print("Not all fields have been given a value")
        return False


# Returns a bool based on if the row can be created
def can_make_row(table, **values):
    try:
        table(**values)
    except TypeError as e:
        print(f"Row cannot be added to {table.__tablename__} - {values} "
              f"Traceback: {e}")
        return False
    else:
        return True
