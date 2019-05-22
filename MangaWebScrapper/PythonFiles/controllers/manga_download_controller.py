import threading
import random
import os
import operator
import collections

import database.database_queries as database_queries
import database.database_enums as database_enums
import resources.constants as constants
import database.database_functions as database_functions
import scrapper.scrapper_manganelo as scrapper_manganelo


class MangaDownloadController(threading.Thread):
    from data_structures.queue import Queue

    queue = Queue()

    def __init__(self):
        super().__init__()

        self.result_named_tuple = collections.namedtuple("Download", "title, chapter")

        self.running = True
        self.current_threads = 0
        self.max_threads = 25
        self.ids_currently_downloading = []
        self.database_gen = self.database_gen()

        self.start()

    def database_gen(self):
        while self.running:
            status = list(e.value for e in database_enums.MangaStatusEnum if e.value <= 3)

            data = database_queries.manga_select_all_in_status_list(status)

            random.shuffle(data)

            for c in data:
                yield c

    def run(self):
        import time

        while self.running:
            thread_available = self.max_threads - self.current_threads >= 1

            if thread_available:
                data = next(self.database_gen)

                # We do not need or want two threads downloading the same Manga
                if data.id not in self.ids_currently_downloading:
                    self.ids_currently_downloading.append(data.id)

                    self.current_threads += 1

                    thread = threading.Thread(target=self.download_thread, daemon=True, args=(data,))

                    thread.start()

            # print(f">>> Concurrent threads: {self.current_threads}")

            time.sleep(0.5)

    def download_thread(self, data):
        # print(f">>> Checking '{data.title}'")

        chapter_list = scrapper_manganelo.ChapterList(data.url)

        chapter_list.start()

        for c in chapter_list:
            # Should be formatted before entering the database - just a double check
            formatted_title = database_functions.remove_nasty_chars(data.title)

            output_dir = os.path.join(constants.MANGA_DIR, formatted_title)
            file_name = f"{formatted_title} Chapter {c.chapter}.pdf"
            file_path = os.path.join(output_dir, file_name)

            os.makedirs(output_dir, exist_ok=True)

            if not os.path.isfile(file_path):
                # ...download chapter here
                download = scrapper_manganelo.ChapterDownload(c.url, file_path)

                download.start()

                if download.success:
                    self.queue.append(self.result_named_tuple(title=formatted_title, chapter=c.chapter))
                else:
                    print(f">>> Failed to download - {formatted_title} {c.chapter}")

        if len(chapter_list) > 0:
            latest_chapter = max(chapter_list, key=operator.attrgetter("chapter"))

            # Update the latest chapter (Previously read from directory which is very slow)
            if latest_chapter.chapter > data.latest_chapter:
                print(f">>> Updating latest chapter for '{data.title[0:25]}' to '{latest_chapter.chapter}'")
                database_queries.manga_update_with_id(data.id, latest_chapter=latest_chapter.chapter)

        self.current_threads -= 1
        self.ids_currently_downloading.remove(data.id)























