import constants
import functions
import time

import selenium.common.exceptions

from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class CiayoBase:
	def __init__(self):
		self.url = None
		self.popup_paths = []
		self.results = []
		self.finished = False

	def start(self):
		if self._setup():
			if self._remove_popup_models():

				self.browser.get(self.url)

				self._extract()

		self.finished = True

		self.browser.quit()

	def _setup(self) -> bool:
		chrome_options = Options()
		chrome_options.headless = True
		# chrome_options.add_experimental_option("detach", True)

		self.browser = Chrome(constants.CHROME_DRIVER_PATH, options=chrome_options)

		self.browser.get(self.url)

		return True

	def _remove_popup_models(self) -> bool:
		for p in self.popup_paths:
			try:
				wait = WebDriverWait(self.browser, 5)

				ele = wait.until(
					EC.presence_of_element_located((By.XPATH, p)))

			except selenium.common.exceptions.TimeoutException:
				return False

			else:
				try:
					ele.click()

				except selenium.common.exceptions.ElementClickInterceptedException:
					return False

			time.sleep(1)

		return True

	def _scroll_to_bottom(self, scroll_delay=0.5):
		last_height = self.browser.execute_script("return document.body.scrollHeight")

		while True:
			self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

			new_height = self.browser.execute_script("return document.body.scrollHeight")

			time.sleep(scroll_delay)

			if new_height == last_height:
				break

			last_height = new_height

	def _extract(self): ...
