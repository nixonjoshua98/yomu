import dataclasses
import requests

from bs4 import BeautifulSoup

from python_files.manganelo.base_class import BaseClass
from python_files.common import functions


@dataclasses.dataclass()
class MangaChapter:
	url: str
	chapter: float


class ChapterList(BaseClass):
	def __init__(self, url: str, *, start: bool = False):
		self.url = url

		self.results = []
		self.finished = False

		if start:
			self.start()

	def start(self):
		self._extract()

		self.finished = True

	def _extract(self):
		page = self._send_request(self.url)

		if page:
			try:
				soup = BeautifulSoup(page.content, "html.parser")

				panel = soup.find(class_="panel-story-chapter-list")
				items = panel.find_all(class_="a-h")

				for i, ele in enumerate(reversed(items)):
					url = ele.find("a")["href"]
					chapter = functions.remove_trailing_zeroes(url.split("chapter_")[-1])

					# Error checks
					url = "http" + url if not url.startswith("http") else url

					self.results.append(MangaChapter(url, chapter))

			except AttributeError:
				pass

			except requests.ConnectionError:
				pass