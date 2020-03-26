import os
import psycopg2
import psycopg2.extras

from configparser import ConfigParser


class DBConnection:
    def __init__(self):
        config = ConfigParser()

        config.read("../postgres.ini")

        self._con = psycopg2.connect(**dict(config.items("postgres")))
        self.cur = self._con.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)

    @staticmethod
    def get_query(file):
        path = os.path.join(os.getcwd(), "queries", file)

        try:
            with open(path, "r") as fh:
                return fh.read()

        except OSError as e:
            print(e)

        return None

    def __enter__(self):
        return self

    def __exit__(self, *args):
        if self._con:
            self._con.commit()
            self.cur.close()
            self._con.close()
