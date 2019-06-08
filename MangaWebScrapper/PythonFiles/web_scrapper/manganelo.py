import functions
import requests
import tempfile
import os

from . import _dataclasses
from .manganelo_base import ManganeloBase

from bs4 import BeautifulSoup
from reportlab.pdfgen import canvas


class Search(ManganeloBase):
	def __init__(self, title):
		super().__init__("panel_story_list", "story_item")

		self.url = functions.create_manganelo_search_url(title)

	def _extract(self):
		for i, ele in enumerate(self.soup):
			story_name = ele.find(class_="story_name").find(href=True)
			story_chap = ele.find(class_="story_chapter").find(href=True)

			row = _dataclasses.SearchResult()

			row.title = story_name.text
			row.desc = story_chap["title"]
			row.url = story_name["href"]

			if not row.url.startswith("http"):
				row.url = "http" + story_name["href"]

			self.results.append(row)


class ChapterList(ManganeloBase):
	def __init__(self, url: str):
		super().__init__("chapter-list", "row")

		self.url = url

	def _extract(self):
		for i, ele in enumerate(reversed(self.soup)):
			chapter = _dataclasses.MangaChapter()

			chapter.url = ele.find("a")["href"]
			chapter.chapter_num = functions.remove_trailing_zeros_if_zero(chapter.url.split("chapter_")[-1])

			if not ele.find("a")["href"].startswith("http"):
				chapter.url = "http" + ele.find("a")["href"]

			self.results.append(chapter)


class ChapterDownload:
	def __init__(self, src_url, dst_path):
		self.src_url = src_url
		self.dst_path = dst_path

		self.image_urls = []
		self.image_paths = []

		self.success = False

	def start(self):
		self.__get_image_urls()

		if len(self.image_urls) > 0:
			with tempfile.TemporaryDirectory() as temp_dir:
				self.__download_images(temp_dir)
				self.__create_pdf()

	def __get_image_urls(self):
		page = functions.send_request(self.src_url)

		if page:
			try:
				soup = BeautifulSoup(page.content, "html.parser")

				image_soup = soup.findAll("img")

				self.image_urls = list(map(lambda i: i["src"], image_soup))

			except (AttributeError, requests.ConnectionError):
				pass

	def __download_images(self, temp_save_dir):
		for i, image_url in enumerate(self.image_urls):
			image_ext = image_url.split(".")[-1]
			image_dst_path = os.path.join(temp_save_dir, f"{i}.{image_ext}")

			if functions.copy_file_url_to_file(image_url, image_dst_path):
				self.image_paths.append(image_dst_path)

	def __create_pdf(self):
		pdf = canvas.Canvas(self.dst_path)

		for image in self.image_paths:
			image_size = functions.get_image_dimensions(image)

			if image_size is not None:
				pdf.setPageSize((image_size.width, image_size.height))
				pdf.drawImage(image, x=0, y=0)
				pdf.showPage()
		try:
			pdf.save()

		except Exception:
			pass

		else:
			self.success = True
