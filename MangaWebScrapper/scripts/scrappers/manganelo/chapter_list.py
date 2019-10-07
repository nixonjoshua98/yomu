
from scripts.scrappers.scrapper_base import ScrapperBase
from bs4 import BeautifulSoup
from dataclasses import dataclass


@dataclass
class MangaChapterDC:
	url: str
	chapter_num: int or float


"""
_function() - Inherited from base class

"""


class ChapterList(ScrapperBase):
	def __init__(self, url: str, start: bool = False):
		self.url = url
		self.soup_list = []

		if start:
			self.start()

	def start(self):
		page = self._send_request(self.url)

		if page is not None:
			try:
				soup = BeautifulSoup(page.content, "html.parser")

				self.soup_list = soup.find(class_="chapter-list").find_all(class_="row")

			except (AttributeError, ConnectionError):
				pass

	def results(self):
		for i, ele in enumerate(reversed(self.soup_list)):
			url = ele.find("a")["href"]
			chapter_num = self._str_to_num(url.split("chapter_")[-1])

			if not ele.find("a")["href"].startswith("http"):
				url = "http" + ele.find("a")["href"]

			yield MangaChapterDC(url, chapter_num)



