from .scrapper_constants import *
from .scrapper_functions import *

from bs4 import BeautifulSoup


class Search(list):
    def __init__(self, title):
        super().__init__()

        self._soup = None
        self.finished = False

        self.search_url = SEARCH_URL + title.replace(" ", "_")

    def start(self):
        self.__get_soup()

        if self._soup is not None:
            self.__get_results()

        self.finished = True

    def __get_soup(self):
        page = send_request(self.search_url)

        if not page:
            return

        try:
            soup = BeautifulSoup(page.content, "html.parser")

            self._soup = soup.find(class_="panel_story_list").find_all(class_="story_item")

        except Exception:
            """ Error has occurred """

    def __get_results(self):
        for i, ele in enumerate(self._soup):
            story_name = ele.find(class_="story_name").find(href=True)
            story_chap = ele.find(class_="story_chapter").find(href=True)

            manga_title = story_name.text
            manga_url = story_name["href"] if story_name["href"].startswith("http") else "http" + story_name["href"]
            latest_chap = story_chap["title"]

            self.append((manga_title, latest_chap, manga_url))


