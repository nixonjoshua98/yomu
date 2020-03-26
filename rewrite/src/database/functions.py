from .dbconnection import DBConnection


def execute_file(file: str, *, limit: int = 1):
	with DBConnection() as con:
		query = con.get_query(file)

		if query is not None:
			con.cur.execute(query, (1,))

			if limit == 1:
				results = con.cur.fetchone()
			else:
				results = con.cur.fetchall()

	return results
