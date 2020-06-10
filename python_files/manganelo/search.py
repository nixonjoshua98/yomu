import dataclasses
import requests

from bs4 import BeautifulSoup

from python_files.manganelo.base_class import BaseClass
from python_files.common import constants


@dataclasses.dataclass()
class MangaSearchResult:
	title: str
	desc: str
	url: str


class Search(BaseClass):
	results = []

	finished = False

	def __init__(self, title):
		self.url = constants.MANGANELO_SEARCH_URL + title.replace(" ", "_")

		self.results = []

		print(self.url)

	def start(self):
		self._extract()

		self.finished = True

	def _extract(self):
		page = self._send_request(self.url)

		if page:
			try:
				soup = BeautifulSoup(page.content, "html.parser")

				panel = soup.find(class_="panel-search-story")
				items = panel.find_all(class_="search-story-item")

				# Iterate over each result
				for i, ele in enumerate(items):
					story_name = ele.find(class_="item-img")
					story_chap = ele.find(class_="item-chapter a-h text-nowrap")

					title, desc, url = story_name["title"], story_chap["title"], story_name["href"]

					# Error checks
					url = "http" + url if not url.startswith("http") else url
					desc = desc.replace(title, "")

					self.results.append(MangaSearchResult(title, desc, url))

			except AttributeError:
				pass

			except requests.ConnectionError:
				pass
