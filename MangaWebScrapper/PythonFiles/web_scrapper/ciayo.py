import constants
import functions
import requests

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options

import time

from . import _dataclasses
from .ciayo_base import CiayoBase


class Search(CiayoBase):
	def __init__(self, title):
		super().__init__()

		self.popup_paths = (
			'//*[@id="AppContainer"]/div[5]/div/div/div[2]/button/div',
			'//*[@id="AppContainer"]/div[4]/div/div/a',
		)

		self.url = functions.create_ciayo_search_url(title)

	def _extract(self):
		self._scroll_to_bottom(1.5)

		for i, c in enumerate(self.browser.find_elements_by_class_name("searchItem")):
			row = _dataclasses.SearchResult()

			if len(c.find_elements_by_class_name("textLabel")) > 0:
				continue

			row.title = c.find_element_by_class_name("searchItem-title").text
			row.url = c.get_attribute("href")
			row.desc = c.find_element_by_class_name("searchItem-genre").text

			self.results.append(row)


class ChapterList(CiayoBase):
	def __init__(self, url: str):
		super().__init__()

		self.popup_paths = (
			'//*[@id="AppContainer"]/div[5]/div/div/a',
		)

		self.url = url

	def _extract(self):
		self._scroll_to_bottom(1.0)

		for c in self.browser.find_elements_by_class_name("comicEpisodeList-item"):
			chapter = _dataclasses.MangaChapter()

			url = c.find_element_by_class_name("comicEpisode").get_attribute("href")

			if url is None:
				continue

			chapter.url = url

			chapter_num = c.find_element_by_class_name("comicEpisode-number").text
			chapter.chapter_num = functions.remove_trailing_zeros_if_zero(chapter_num.replace("Episode", ""))

			self.results.append(chapter)





