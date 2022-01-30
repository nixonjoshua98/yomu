import threading
import time
from src import datasources
from src.storage import JSONStorage


class UpdateWorker(threading.Thread):
    def __init__(self, data_storage: JSONStorage):
        super(UpdateWorker, self).__init__(daemon=True)

        self.data: JSONStorage = data_storage

    def run(self) -> None:

        while self.is_alive():
            self.data.backup()

            for status in (0, 1, 2, 3):

                for story in self.data.get_stories_with_status(status):
                    source = datasources.get_data_source(story)

                    try:
                        # Chapters may not have been found
                        if not (chapters := source.get_chapters(url=story.url)):
                            continue

                        latest = max(chapters, key=lambda chap: chap.chapter)

                        story.source_id = latest.source_id

                        # Update the chapters latest chapter
                        if latest.chapter != story.latest_chapter:
                            story.latest_chapter = latest.chapter

                            self.data.update_story(story)

                    except: ...

                    time.sleep(0.2)

            time.sleep(180)
