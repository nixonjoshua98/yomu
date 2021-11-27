import functools as ft
import json
import os
import secrets
from threading import Lock as ThreadLock
from typing import KeysView, Optional, Union
import datetime as dt
from src.models import Story


@ft.cache
def get():
    return JSONStorage()


class JSONStorage:
    def __init__(self):
        self._lock = ThreadLock()

    @property
    def data_file_name(self):
        return os.path.join(os.getcwd(), "stories.json")

    def update_story(self, story: Story):
        self._update_data_file_key({story.id: story.dict()})

    def get_stories_with_status(self, status: int, *, readable_only: bool = False) -> list[Story]:
        stories = [s for s in self.get_all_stories() if s.status_value == status]

        if readable_only:
            stories = [s for s in stories if s.latest_chapter > s.chapters_read]

        return sorted(stories, key=lambda s: s.latest_chapter - s.chapters_read)

    def get_all_stories(self) -> list[Story]:
        data = self.read_stories_file()

        return [Story.parse_obj(s) for s in data.values()]

    def insert_story(self, title, url, status) -> Story:
        return self._insert_story(title, url, status)

    def delete_story(self, story: Story):
        self._remove_data_file_key(story.id)

    def get_story(self, story_id) -> Optional[Story]:
        story_dict = self.read_stories_file().get(story_id)

        return Story.parse_obj(story_dict) if story_dict else None

    def read_stories_file(self) -> dict:
        with open(self.data_file_name, "r") as fh:
            d: dict = json.load(fh, object_hook=_JsonHooks.load_object_hook)

            return {k: {"storyId": k, **v} for k, v in d.items()}

    def _insert_story(self, title, url, status) -> Story:
        stories: dict = self.read_stories_file()

        story = Story(
            storyId=self._get_unique_key(stories.keys()),
            title=title,
            url=url,
            status=status,
        )

        self._update_data_file_key({story.id: story.dict()})

        return story

    def _update_data_file_key(self, data: dict):
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

    @staticmethod
    def _get_unique_key(existing_keys: Union[list[str], KeysView[str]]) -> str:
        while (key := secrets.token_hex(8)) in existing_keys:
            ...

        return key


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
