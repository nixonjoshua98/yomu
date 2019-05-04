from sqlalchemy.inspection import inspect


def all_fields_have_value(table, fields_given, ignore_pk = True):
    table_fields = table.__table__.columns.keys()

    if ignore_pk:
        pk = inspect(table).primary_key[0].name
        table_fields.remove(pk)

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
        print(f"Row cannot be added to {table.__tablename__}")
        return False
    else:
        return True
