import functions
import data_classes
import time

from .ciayo_base import CiayoBase

from web_scrapper.download_base import DownloadBase
from bs4 import BeautifulSoup


class Search(CiayoBase):
	def __init__(self, title):
		super().__init__(functions.create_ciayo_search_url(title))

		self.popup_paths = (
			'//*[@id="AppContainer"]/div[5]/div/div/div[2]/button/div',
			'//*[@id="AppContainer"]/div[4]/div/div/a',
		)

	def extract(self):
		self.scroll_to_bottom(1.5)

		for i, c in enumerate(self.browser.find_elements_by_class_name("searchItem")):
			row = data_classes.SearchResult()

			if len(c.find_elements_by_class_name("textLabel")) > 0:
				continue

			row.title = c.find_element_by_class_name("searchItem-title").text
			row.url = c.get_attribute("href")
			row.desc = c.find_element_by_class_name("searchItem-genre").text

			self.results.append(row)


class ChapterList(CiayoBase):
	def __init__(self, url: str):
		super().__init__(url)

		self.popup_paths = (
			'//*[@id="AppContainer"]/div[5]/div/div/a',
		)

	def extract(self):
		self.scroll_to_bottom(1.0)

		for c in self.browser.find_elements_by_class_name("comicEpisodeList-item"):
			chapter = data_classes.MangaChapter()

			url = c.find_element_by_class_name("comicEpisode").get_attribute("href")

			chapter_num = c.find_element_by_class_name("comicEpisode-number").text
			chapter_num = functions.remove_trailing_zeros_if_zero(chapter_num.replace("Episode", ""))

			if url is None or not functions.is_float(chapter_num):
				continue

			chapter.url = url
			chapter.chapter_num = chapter_num

			self.results.insert(0, chapter)


class ChapterDownload(DownloadBase, CiayoBase):
	def __init__(self, src_url, dst_path):
		DownloadBase.__init__(self, src_url, dst_path)
		CiayoBase.__init__(self, src_url)

	def extract(self):
		for i, ele in enumerate(self.browser.find_elements_by_class_name("chapterViewer-slice")):
			img = ele.find_element_by_tag_name("img")

			if img is not None:
				self.image_urls.append(img.get_attribute("src"))

	def get_image_urls(self):
		""" Done in .extract as twin inheritance """

	def start(self):
		CiayoBase.start(self)
		DownloadBase.start(self)


