import requests
import os
import tempfile

from bs4 import BeautifulSoup
from reportlab.pdfgen import canvas

from python_files.manganelo.base_class import BaseClass


class ChapterDownload(BaseClass):
	def __init__(self, src_url, dst_path):
		self._src_url = src_url
		self._dst_path = dst_path

		self._downloaded_images = []

		self.success = False

	def start(self):
		image_urls = self._get_image_urls()

		# No images found, so finish here
		if len(image_urls) == 0:
			return

		with tempfile.TemporaryDirectory() as temp_dir:
			self._download_image_urls(image_urls, temp_dir)

			self.create_pdf()

	def _get_image_urls(self) -> list:
		page = self._send_request(self._src_url)

		image_urls = []

		if page:
			try:
				soup = BeautifulSoup(page.content, "html.parser")
				image_soup = soup.findAll("img")
				image_urls = [ele["src"] for ele in image_soup]

			except (AttributeError, requests.ConnectionError) as e:
				pass

		return image_urls

	def _download_image_urls(self, image_urls: list, temp_save_dir: str):
		for i, image_url in enumerate(image_urls):
			image_ext = image_url.split(".")[-1]

			image_dst_path = os.path.join(temp_save_dir, f"{i}.{image_ext}")

			if self._download_url(image_url, image_dst_path):
				self._downloaded_images.append(image_dst_path)

	def create_pdf(self):
		pdf = canvas.Canvas(self._dst_path)

		for image in self._downloaded_images:
			image_size = self._get_image_size(image)

			if image_size is not None:
				pdf.setPageSize((image_size.w, image_size.h))

				try:
					pdf.drawImage(image, x=0, y=0)
				except OSError as e:
					print(e)
					continue

				pdf.showPage()

		pdf.save()

		self.success = True
