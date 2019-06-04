import collections
import shutil
import PIL
import os
import tempfile

from .scrapper_constants import *
from .scrapper_functions import *
from reportlab.pdfgen import canvas

from bs4 import BeautifulSoup

import functions.helper_functions as helper_functions


class Search(list):
    def __init__(self, title):
        super().__init__()

        self.__soup = None
        self.finished = False

        self.search_url = SEARCH_URL + title.replace(" ", "_")

    def start(self):
        self.__get_soup()

        if self.__soup is not None:
            self.__get_results()

        self.finished = True

    def __get_soup(self):
        page = send_request(self.search_url)

        if not page:
            return

        try:
            soup = BeautifulSoup(page.content, "html.parser")

            self.__soup = soup.find(class_="panel_story_list").find_all(class_="story_item")

        except (AttributeError, requests.ConnectionError):
            """ Error has occurred """

    def __get_results(self):
        for i, ele in enumerate(self.__soup):
            story_name = ele.find(class_="story_name").find(href=True)
            story_chap = ele.find(class_="story_chapter").find(href=True)

            row = dict()

            row["title"] = story_name.text
            row["latest_chapter"] = story_chap["title"]
            row["url"] = story_name["href"] if story_name["href"].startswith("http") else "http" + story_name["href"]

            self.append(row)


class ChapterList(list):
    def __init__(self, url: str):
        super().__init__()

        self.url = url

        self.__soup = None

    def start(self):
        self.__get_soup()

        if self.__soup is not None:
            self.__get_results()

    def __get_soup(self):
        page = send_request(self.url)

        if not page:
            return

        try:
            soup = BeautifulSoup(page.content, "html.parser")

            self.__soup = soup.find(class_="chapter-list").findAll(class_="row")

        except (AttributeError, requests.ConnectionError):
            """ Error has occurred """

    def __get_results(self):
        result_named_tuple = collections.namedtuple("Chapter", "chapter, url")

        for i, ele in enumerate(reversed(self.__soup)):
            url = ele.find("a")["href"] if ele.find("a")["href"].startswith("http") else "http" + ele.find("a")["href"]
            num = url.split("chapter_")[-1]

            self.append(result_named_tuple(helper_functions.remove_trailing_zeros_if_zero(num), url))


class ChapterDownload:
    def __init__(self, url, file_out):
        self.url = url
        self.image_urls = []
        self.image_paths = []
        self.chapter_save_dir = file_out

        self.success = False

    def start(self):
        self.__get_image_urls()

        if len(self.image_urls) > 0:
            with tempfile.TemporaryDirectory() as temp_dir:

                self.__download_images(temp_dir)
                self.__create_pdf()

    def __get_image_urls(self):
        page = send_request(self.url)

        if page:
            try:
                soup = BeautifulSoup(page.content, "html.parser")

                image_soup = soup.findAll("img")

                self.image_urls = list(map(lambda i: i["src"], image_soup))

            except (AttributeError, requests.ConnectionError) as e:
                print(self.url, e, sep=" | ")

    def __download_images(self, temp_save_dir):
        for i, image_url in enumerate(self.image_urls):
            image_ext = image_url.split(".")[-1]
            image_path = os.path.join(temp_save_dir, f"{i}.{image_ext}")
            image_file = send_request(image_url)

            if image_file:
                with open(image_path, "wb") as f:
                    image_file.raw.decode_content = True

                    try:
                        shutil.copyfileobj(image_file.raw, f)
                    except Exception as e:  # Too broad
                        """ Error """
                    else:
                        self.image_paths.append(image_path)

    def __create_pdf(self):
        pdf = canvas.Canvas(self.chapter_save_dir)

        for image in self.image_paths:
            try:
                with PIL.Image.open(image) as img:
                    w, h = img.size

                pdf.setPageSize((w, h))
                pdf.drawImage(image, x=0, y=0)
                pdf.showPage()

            except OSError as e:
                print(f">>> Filed to create chapter - {e}")

        try:
            pdf.save()
        except Exception as e:
            print(self.chapter_save_dir, e, sep=" | ")
            """ Error occurred """
        else:
            self.success = True







