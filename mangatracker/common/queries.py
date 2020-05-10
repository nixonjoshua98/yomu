
class MangaSQL:
    TABLE = "CREATE TABLE IF NOT EXISTS manga(" \
            "mangaID INTEGER PRIMARY KEY," \
            "title VARCHAR(256)," \
            "url VARCHAR(256)," \
            "chapters_read FLOAT," \
            "latest_chapter FLOAT," \
            "status INTEGER" \
            ");"

    SELECT_STATUS = "SELECT * FROM manga WHERE status = ?;"
