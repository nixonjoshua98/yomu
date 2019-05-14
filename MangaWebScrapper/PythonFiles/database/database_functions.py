from sqlalchemy.inspection import inspect


def get_non_pk_fields(tbl) -> list:
	table_fields = tbl.__table__.columns.keys()
	pk = get_table_pk(tbl)
	table_fields.remove(pk)
	return table_fields


def get_table_pk(tbl) -> str:
	return inspect(tbl).primary_key[0].name
