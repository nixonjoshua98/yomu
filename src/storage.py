import subprocess

from bson import ObjectId
from pymongo import MongoClient

__storage_inst = None

"""
    mangaId [_id]: Unique
    title
    url
    status
    latest_chapter
    chapters_read
"""

"""
    The purpose of abstract storage is so we can access different formats (Mongo, JSON, SQL etc.) via the same methods,
    the internal fields may be different but the returned field names should be the same as above.
"""


class AbstractDataStorage:

    def backup(self, output): ...

    def insert_one(self, row: dict): ...

    def delete_one(self, iid): ...

    def update_one(self, iid, new_fields: dict): ...

    def find_one(self, iid): ...

    def get_all_with_status(self, status: int, *, readable_only: bool = False) -> list: ...


class MongoStorage(AbstractDataStorage):
    def __init__(self):
        self._client = MongoClient()

    @property
    def _database(self):
        return self._client["manga"]

    @property
    def _collection(self):
        return self._database["manga"]

    def delete_one(self, iid):
        self._collection.delete_one({"_id": self._str_to_bson(iid)})

    def backup(self, output):
        subprocess.call(f'mongodump.exe -d {self._database.name} -o "{output}"', shell=True)

    def insert_one(self, row: dict):
        self._collection.insert_one(row)

    def find_one(self, iid):
        row = self._collection.find_one({"_id": self._str_to_bson(iid)})

        # '_rename_keys' takes a list, so we send as a list then take the first element
        return [row][0] if row else row

    def update_one(self, iid, new_fields: dict):
        self._collection.update_one({"_id": self._str_to_bson(iid)}, {"$set": {k: v for k, v in new_fields.items()}})

    def get_all_with_status(self, status: int, *, readable_only: bool = False) -> list:

        match: dict = {"$match": {"status": status}}

        if readable_only:
            match["$match"]["$and"] = [{"numAvailableChapters": {"$gt": 0}}]

        pipeline = [
            {"$addFields": {"numAvailableChapters": {"$subtract": ["$latest_chapter", "$chapters_read"]}}},
            match,
            {"$sort": {"numAvailableChapters": -1}}
        ]

        return self._aggregate(pipeline)

    def _find(self, query):
        return list(self._collection.find(query))

    def _aggregate(self, pipeline):
        return list(self._collection.aggregate(pipeline))

    @staticmethod
    def _str_to_bson(s):
        """ Converts a 'str' to 'ObjectId' used in MongoDB. """

        if isinstance(s, (str,)):
            return ObjectId(s)

        return s


def get():
    global __storage_inst

    if __storage_inst is None:
        __storage_inst = MongoStorage()

    return __storage_inst
