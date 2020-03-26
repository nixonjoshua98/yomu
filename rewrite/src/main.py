
if __name__ == "__main__":
    import os
    import sys

    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    
    from src.interface import Application
    from src.database import DBConnection

    with DBConnection() as con:
        query = con.get_query("createmangatable.sql")

        if query is not None:
            con.cur.execute(query)

    app = Application()

    app.mainloop()
