import os
import shutil
import threading

from scripts import data


class CleanupWorker(threading.Thread):
	def __init__(self, manga, callback):
		super(CleanupWorker, self).__init__(daemon=True)

		self.manga = manga
		self.callback = callback

	def run(self):
		files_removed = 0

		for m in self.manga:
			manga_save_dir = os.path.join(data.paths.MANGA_SAVE_DIR, m.title)

			if os.path.isdir(manga_save_dir):
				# Remove directories which I have dropped or completed and are not being downloaded
				if not data.manga_status.from_key(m.status).downloadable:
					shutil.rmtree(manga_save_dir)
					files_removed += len(os.listdir(manga_save_dir))
					continue

				# Remove old chapters
				for file in os.listdir(manga_save_dir):
					file_path = os.path.join(manga_save_dir, file)

					chapter_num = file.replace(f"{m.title} Chapter", "").replace(".pdf", "")

					if float(chapter_num) < m.chapters_read:
						try:
							os.remove(file_path)
							files_removed += 1
						except FileNotFoundError as e:
							print(f"cleanup_worker.py - {e}")
							continue

		dir_set = set(os.listdir(data.paths.MANGA_SAVE_DIR))
		manga_title_set = set(map(lambda ma: ma.title, self.manga))

		# Delete manga which are not in the database
		for deleted_title in (dir_set - manga_title_set):
			dir_path = os.path.join(data.paths.MANGA_SAVE_DIR, deleted_title)
			shutil.rmtree(dir_path)
			files_removed += len(os.listdir(dir_path))

		self.callback(files_removed)

