import os

# Full path to the database which will be used
DB_PATH = os.path.join(os.path.dirname(os.getcwd()), "Resources", "manga_database.sqlite3")

# Connection string used in SQLAlchemy
CON_STR = "sqlite:///" + DB_PATH