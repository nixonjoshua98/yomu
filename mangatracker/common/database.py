import sqlite3

from mangatracker import utils


def dict_cursor_factory(cur, row): return {col[0]: row[i] for i, col in enumerate(cur.description)}


class Database:
    def __init__(self, db: str = None):
        self._db = db if db is not None else utils.user_data.get("database", "path")
        self._cur_factory = dict_cursor_factory

    def fetch(self, query: str, *params):
        with sqlite3.connect(self._db) as con:
            con.row_factory = self._cur_factory

            c = con.cursor()

            c.execute(query, params)

            results = c.fetchall()

        return results

    def execute(self, query, *params) -> bool:
        with sqlite3.connect(self._db) as con:
            c = con.cursor()

            c.execute(query, params)

        return True
