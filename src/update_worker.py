import threading
import time

from src import datasources
from src.data_repository import DataRepository


class UpdateWorker(threading.Thread):
    def __init__(self, data_storage: DataRepository):
        super(UpdateWorker, self).__init__(daemon=True)

        self.repository: DataRepository = data_storage

    def run(self) -> None:

        while self.is_alive():
            for status in (0, 1, 2, 3):

                for story in self.repository.get_stories_with_status(status):
                    source = datasources.get_data_source(story)

                    try:
                        # Chapters may not have been found
                        if not (chapters := source.get_chapters(url=story.url)):
                            continue

                        latest = max(chapters, key=lambda chap: chap.chapter)

                        # Update the chapters latest chapter
                        if latest.chapter != story.latest_chapter:
                            story.latest_chapter = latest.chapter

                            self.repository.update(story)

                    except:
                        ...

                    time.sleep(0.2)

            time.sleep(180)
