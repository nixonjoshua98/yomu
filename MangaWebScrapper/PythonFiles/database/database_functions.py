from sqlalchemy.inspection import inspect


def get_non_pk_fields(tbl) -> list:
	table_fields = tbl.__table__.columns.keys()
	pk = get_table_pk(tbl)
	table_fields.remove(pk)
	return table_fields


def get_table_pk(tbl) -> str:
	return inspect(tbl).primary_key[0].name


def get_enums_from_enum_field(tbl, field: str):
	if hasattr(tbl, field):
		try:
			s = getattr(tbl, field).property.columns[0].type.enums
		except AttributeError as e:
			return False
		else:
			return s
	else:
		raise Exception(f"Table {tbl.__tablename__} has no column named '{field}'")
