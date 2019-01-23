from bs4 import BeautifulSoup

import functions.serverRequest as serverRequest

import functions.functions as funcs

class ChapterList(list):
    def __init__(self, menuUrl):
        self.menuUrl     = menuUrl
        self.chapterSoup = []

        if (self.scrape()):
            self.extract()


    def scrape(self):
        page = serverRequest.sendRequest(self.menuUrl)

        if (page == False):
            return False

        try:
            soup = BeautifulSoup(page.content, "html.parser")
            rawChapList = soup.find(class_ = "chapter-list")
            
            self.chapterSoup = rawChapList.findAll(class_ = "row")
        except Exception:
            """ Error occurred when trying to get each chapter row """
            return False
        else:
            return True


    def extract(self):
        for i, row in enumerate(self.chapterSoup[::-1]):
            chapterUrl = row.find("a")["href"]

            if (not chapterUrl.startswith("https:")):
                chapterUrl = "https:" + chapterUrl
                
            chapterNum = chapterUrl.split("chapter_")[-1]
            
            self.append([chapterUrl, funcs.parseToNumber(chapterNum)])
            
