import sqlite3

import data.constants as consts

# Static class
from classes.comicStatus import ComicStatus

class Database:
    @classmethod
    def query(cls, sql, values = None):
        with sqlite3.connect(consts.databasePath) as db:
            cursor = db.cursor()

            if (values != None):
                cursor.execute(sql, values)
            else:
                cursor.execute(sql)
            
        db.commit()

        return cursor.fetchall()

    @classmethod
    def createTable(cls):
        sql = (
            "CREATE TABLE IF NOT EXISTS COMICS("
            "comic_id INTEGER PRIMARY KEY, "
            "comic_title TEXT, "
            "menu_url TEXT, "
            "chapter_url TEXT, "
            "chapters_read TEXT, "
            "comic_status INTEGER)"
            )
        Database.query(sql)

    @classmethod
    def getViewableComics(cls, comicStatus):
        values = (comicStatus,)
        
        sql = (
            "SELECT comic_title, chapters_read "
            "FROM COMICS "
            "WHERE comic_status = ?"
            )
        
        return Database.query(sql, values)

    @classmethod
    def getAll(cls, comicStatus):
        values = (comicStatus,)
        
        sql = "SELECT * FROM COMICS"
        
        return Database.query(sql, values)

    @classmethod
    def getDownloadableComics(cls):
        # Gets all comic statuses which are allowed to be downloaded
        values = [str(i) for i in ComicStatus.allId() if ComicStatus.idToDownloadable(i)]

        sql = (
            "SELECT comic_id, comic_title, menu_url "
            "FROM COMICS "
            "WHERE comic_status IN ({0})".format(", ".join(values))
            )

        return Database.query(sql)

    @classmethod
    def updateComic(cls, comicTitle, comicStatus, chaptersRead):
        comicTitle = comicTitle.replace('"', "'")
        values     = (str(chaptersRead), comicStatus, comicTitle,)

        sql = (
            "UPDATE COMICS "
            "SET chapters_read = ?, comic_status = ? "
            "WHERE comic_title = ?"
            )

        Database.query(sql, values)

    @classmethod
    def comicExists(cls, comicTitle):
        comicTitle = comicTitle.replace('"', "'")
        
        sql = (
            "SELECT comic_id "
            "FROM COMICS "
            "WHERE comic_title = ?"
            )
        return len(Database.query(sql, (comicTitle,))) != 0

    @classmethod
    def addRow(cls, comicTitle, menuUrl, chapterUrl):
        values = (comicTitle, menuUrl, chapterUrl, 0, 0)
        sql = (
            "INSERT INTO COMICS("
            "comic_title, menu_url, chapter_url, chapters_read, comic_status) "
            "VALUES (?, ?, ?, ?, ?)"
            )
        Database.query(sql, values)

    @classmethod
    def getMenuUrl(cls, comicTitle):
        sql = (
            "SELECT menu_url "
            "FROM COMICS "
            "WHERE comic_title = ?"
            )
        return Database.query(sql, (comicTitle.replace('"', "'"),))



Database.createTable()
