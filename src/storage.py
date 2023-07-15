import functools as ft
from bson import ObjectId
from typing import Optional, Union
from src.models.story import Story
from pymongo import MongoClient


@ft.cache
def get_instance():
    return MongoRepository()


class MongoRepository:
    def __init__(self):
        mongo = MongoClient()

        self._collection = mongo["yomu"]["stories"]

    def update_story(self, story: Story):
        self._collection.update_one({"_id": story.id}, {"$set": story.dict()})

    def get_stories_with_status(self, status: int, *, readable_only: bool = False) -> list[Story]:
        stories = [Story.parse_obj(s) for s in list(self._collection.find({"status": status}))]

        if readable_only:
            stories = [s for s in stories if s.latest_chapter > s.chapters_read]

        return sorted(stories, key=lambda s: (s.latest_chapter - s.chapters_read, s.title))

    def get_readable_stories(self) -> list[Story]:
        pipeline = [
            {
                "$match": {
                    "$expr": {
                        "$gt": ["$latestChapter", "$latestChapterRead"]
                    },
                    "status": {"$in": [0, 2]}
                }
            }
        ]

        ls = self._collection.aggregate(pipeline)

        return [Story.parse_obj(s) for s in ls]

    def get_all_stories(self) -> list[Story]:
        return [Story.parse_obj(s) for s in list(self._collection.find())]

    def insert_story(self, story: Story):
        self._collection.insert_one(story.dict())

    def delete_story(self, story: Story):
        self._collection.delete_one({"_id": story.id})

    def get_story(self, story_id: Union[str, ObjectId]) -> Optional[Story]:
        story_id = story_id if isinstance(story_id, ObjectId) else ObjectId(story_id)

        story = self._collection.find_one({"_id": story_id})

        return Story.parse_obj(story) if story else None
