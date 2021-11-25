import functools as ft
import json
import os
import secrets
from threading import Lock as ThreadLock
from typing import KeysView, Optional, Union

from src.models import Story


class JSONStorage:
    def __init__(self):
        self._lock = ThreadLock()

    @property
    def data_file_name(self):
        return os.path.join(os.getcwd(), "stories.json")

    def update_one(self, story: Story):
        self._update_stories_data_file({story.id: story.dict()})

    def get_all_with_status(self, status: int, *, readable_only: bool = False) -> list[Story]:
        stories = [s for s in self.get_all_stories() if s.status_int == status]

        if readable_only:
            stories = [s for s in stories if s.latest_chapter > s.chapters_read]

        return sorted(stories, key=lambda s: s.latest_chapter - s.chapters_read)

    def get_all_stories(self) -> list[Story]:
        data = self.read_stories_file()

        return [Story.parse_obj(s) for s in data.values()]

    def insert_one(self, title, url, status):
        self._insert_story(title, url, status)

    def find_one(self, story_id) -> Optional[Story]:
        story_dict = self.read_stories_file().get(story_id)

        return Story.parse_obj(story_dict) if story_dict else None

    def read_stories_file(self) -> dict:
        with open(self.data_file_name, "r") as fh:
            return {k: {"storyId": k, **v} for k, v in json.load(fh).items()}

    def _insert_story(self, title, url, status):
        stories: dict = self.read_stories_file()

        story = Story(
            storyId=self._get_unique_key(stories.keys()),
            title=title,
            url=url,
            status=status,
        )

        self._update_stories_data_file({story.id: story.dict()})

    @staticmethod
    def _find_one_story(data, story_id) -> dict:
        return data.get(story_id)

    def _update_stories_data_file(self, data: dict):
        old_file = self.read_stories_file()
        new_file = {**old_file, **data}

        try:
            with self._lock, open(self.data_file_name, "w") as fh:
                json.dump(new_file, fh, indent=2)

        except json.JSONDecodeError:
            self._update_stories_data_file(old_file)

    @staticmethod
    def _get_unique_key(existing_keys: Union[list[str], KeysView[str]]) -> str:
        while (key := secrets.token_hex(8)) in existing_keys:
            ...

        return key


@ft.cache
def get():
    return JSONStorage()
