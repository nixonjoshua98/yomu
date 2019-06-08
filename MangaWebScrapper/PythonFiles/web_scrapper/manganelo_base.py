import functions
import requests
import tempfile
import os

from . import _dataclasses

from bs4 import BeautifulSoup
from reportlab.pdfgen import canvas


class ManganeloBase:
	def __init__(self, find_class, find_all_class):
		self.find_class = find_class
		self.find_all_class = find_all_class

		self.results = []
		self.soup = []
		self.finished = False
		self.url = None

	def start(self):
		self._get_soup()

		if self.soup is not None:
			self._extract()

		self.finished = True

	def _get_soup(self):
		page = functions.send_request(self.url)

		if page:
			try:
				soup = BeautifulSoup(page.content, "html.parser")

				self.soup = soup.find(class_=self.find_class).find_all(class_=self.find_all_class)

			except (AttributeError, requests.ConnectionError):
				pass

	def _extract(self): ...
