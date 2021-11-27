import json
import threading
import time

from src import utils
from src.datasources import (AbstractDataSource, DataSourceChapter,
                             MangaKatanaDataSource, ManganeloDataSource)
from src.errors import StoryNotFound
from src.models import Story
from src.storage import JSONStorage


class UpdateWorker(threading.Thread):
    def __init__(self, data_storage: JSONStorage):
        super(UpdateWorker, self).__init__(daemon=True)

        self._data_storage: JSONStorage = data_storage

    def run(self) -> None:

        while self.is_alive():
            self.backup_json()
            
            for status in (0, 1, 2, 3):
                results: list[Story] = self._data_storage.get_stories_with_status(status)

                for story in results:
                    source = self.get_source(story.url)

                    try:
                        if not (chapters := source.get_chapters(url=story.url)):
                            continue

                    except StoryNotFound:
                        self.update_missing_story(source, story)

                    else:
                        latest = max(chapters, key=lambda chap: chap.chapter)

                        if latest.chapter != story.latest_chapter:
                            self.update_story_latest_chapter(story.copy(), latest)

                    time.sleep(0.2)

            time.sleep(60)

    def update_missing_story(self, source: AbstractDataSource, story: Story):
        if story.can_update_missing_story():
            story.last_missing_story_check = utils.utcnow()

            for search_result in source.search(story.title):
                if search_result.title == story.title:
                    story.url = search_result.url

            self._data_storage.update_story(story)

    def update_story_latest_chapter(self, story: Story, chapter: DataSourceChapter):
        story.latest_chapter = chapter.chapter

        self._data_storage.update_story(story)

    def backup_json(self):
        with open(
                f"E:\\OneDrive\\Backups\\Yomu\\stories-{int(utils.utcnow().timestamp())}.json",
                "w+",
        ) as fh:
            json.dump(self._data_storage.read_stories_file(), fh, indent=2)

    @staticmethod
    def get_source(url: str) -> AbstractDataSource:
        if any(map(lambda ele: ele in url, ("manganelo", "manganato"))):
            return ManganeloDataSource

        return MangaKatanaDataSource
