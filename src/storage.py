import functools as ft
import json
import os
from src import utils
from threading import Lock as ThreadLock
from typing import Optional
import datetime as dt
from src.models import Story


@ft.cache
def get_instance():
    return JSONStorage()


class JSONStorage:
    def __init__(self):
        self._lock = ThreadLock()

    @property
    def data_file_name(self):
        return os.path.join(os.getcwd(), "stories.json")

    def update_story(self, story: Story):
        self._append_data_file({story.id: story.dict()})

    def get_stories_with_status(self, status: int, *, readable_only: bool = False) -> list[Story]:
        stories = [s for s in self.get_all_stories() if s.status_value == status]

        if readable_only:
            stories = [s for s in stories if s.latest_chapter > s.chapters_read]

        return sorted(stories, key=lambda s: s.latest_chapter - s.chapters_read)

    def get_all_stories(self) -> list[Story]:
        data = self.read_stories_file()

        return [Story.parse_obj(s) for s in data.values()]

    def insert_story(self, story: Story):
        self._append_data_file({story.id: story.dict()})

    def delete_story(self, story: Story):
        self._remove_data_file_key(story.id)

    def get_story(self, story_id) -> Optional[Story]:
        story_dict = self.read_stories_file().get(story_id)

        return Story.parse_obj(story_dict) if story_dict else None

    def read_stories_file(self) -> dict:
        with open(self.data_file_name, "r") as fh:
            d: dict = json.load(fh, object_hook=_JsonHooks.load_object_hook)

            return {k: {"storyId": k, **v} for k, v in d.items()}

    def backup(self):
        f = f"E:\\OneDrive\\Backups\\Yomu\\stories-{int(utils.utcnow().timestamp())}.json"

        with open(f, "w+",) as fh:
            json.dump(self.read_stories_file(), fh, indent=2, default=_JsonHooks.dump_default)

    def _append_data_file(self, data: dict):
        old_file = self.read_stories_file()
        self._write_stories_data_file({**old_file, **data})

    def _remove_data_file_key(self, key: str):
        data = self.read_stories_file()
        data.pop(key, None)
        self._write_stories_data_file(data)

    def _write_stories_data_file(self, data: dict):
        old_file = self.read_stories_file()

        try:
            with self._lock, open(self.data_file_name, "w") as fh:
                json.dump(data, fh, indent=2, default=_JsonHooks.dump_default)

        except (TypeError, json.JSONDecodeError):
            self._write_stories_data_file(old_file)


class _JsonHooks:

    @staticmethod
    def dump_default(x):
        if isinstance(x, (dt.datetime,)):
            return {"_isoformat": x.isoformat()}
        return str(x)

    @staticmethod
    def load_object_hook(x):
        if (iso := x.get('_isoformat')) is not None:
            return dt.datetime.fromisoformat(iso)
        return x
