import functions
import requests

from .manganelo_base 			import ManganeloBase
from web_scrapper.download_base import DownloadBase
from data_classes 				import (MangaSearchResult, MangaDataClass)
from bs4 						import BeautifulSoup


class Search(ManganeloBase):
	def __init__(self, title):
		super().__init__("panel-search-story", "search-story-item")

		self.url = self.MANGANELO_SEARCH_URL + title.replace(" ", "_")

	def _extract(self):
		for i, ele in enumerate(self.soup):
			story_name = ele.find(class_="item-img")
			story_chap = ele.find(class_="item-chapter a-h text-nowrap")

			row = MangaSearchResult()

			row.title = story_name["title"]
			row.desc = story_chap["title"]
			row.url = story_name["href"]

			if not row.url.startswith("http"):
				row.url = "http" + story_name["href"]

			self.results.append(row)


class ChapterList(ManganeloBase):
	def __init__(self, url: str):
		super().__init__("panel-story-chapter-list", "a-h")

		self.url = url

	def _extract(self):
		for i, ele in enumerate(reversed(self.soup)):
			chapter = MangaDataClass()

			chapter.url = ele.find("a")["href"]
			chapter.chapter = functions.remove_trailing_zeros_if_zero(chapter.url.split("chapter_")[-1])

			if not ele.find("a")["href"].startswith("http"):
				chapter.url = "http" + ele.find("a")["href"]

			self.results.append(chapter)


class ChapterDownload(DownloadBase):
	def __init__(self, src_url, dst_path):
		super().__init__(src_url, dst_path)

		self.image_urls = []

	def get_image_urls(self):
		page = functions.send_request(self.src_url)

		if page:
			try:
				soup = BeautifulSoup(page.content, "html.parser")

				image_soup = soup.findAll("img")

				self.image_urls = list(map(lambda i: i["src"], image_soup))

			except (AttributeError, requests.ConnectionError) as e:
				print(e)
