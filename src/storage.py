import subprocess
import re

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

    def find(self, **kwargs): ...

    def find_one(self, iid): ...

    def get_with_title(self, title: str, *, ignore_case: bool = True) -> list: ...

    def get_with_status(self, status: int, *, readable_only: bool = False) -> list:...


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
        return self._rename_keys([row])[0] if row else row

    def find(self, query):
        return list(self._collection.find(query))

    def update_one(self, iid, new_fields: dict):
        self._collection.update_one({"_id": self._str_to_bson(iid)}, {"$set": {k: v for k, v in new_fields.items()}})

    def get_with_title(self, title, *, ignore_case: bool = True) -> list:
        return self.find({"title": re.compile(title, re.IGNORECASE)})

    def get_with_status(self, status: int, *, readable_only: bool = False) -> list:

        match: dict = {"$match": {"status": status}}

        if readable_only:
            match["$match"]["$and"] = [{"numAvailableChapters": {"$gt": 0}}]

        pipeline = [
            {
                "$addFields": {"numAvailableChapters": {"$subtract": ["$latest_chapter", "$chapters_read"]}}
            },
            match,
            {
                "$sort": {"numAvailableChapters": -1}
            }
        ]

        return self._aggregate(pipeline)

    def _aggregate(self, pipeline):
        return self._rename_keys(list(self._collection.aggregate(pipeline)))

    @staticmethod
    def _rename_keys(ls: list):
        renames = {"_id": "mangaId"}

        for i, ele in enumerate(ls):
            for old_key, new_key in renames.items():
                ele[new_key] = ele.pop(old_key)

        return ls

    @staticmethod
    def _str_to_bson(s):
        """ Converts a 'str' to 'ObjectId' used in MongoDB. """

        if isinstance(s, (str,)):
            return ObjectId(s)

        return s


def get_instance():
    global __storage_inst

    if __storage_inst is None:
        __storage_inst = MongoStorage()

    return __storage_inst
