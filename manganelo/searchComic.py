from bs4 import BeautifulSoup

import functions.serverRequest as serverRequest

import functions.functions as funcs

class SearchComic(list):
    def __init__(self, comicTitle):
        self.url = "http://manganelo.com/search/" + comicTitle.replace(" ", "_").lower()
        self.soupSearchResults = []

        if (self.scrape()):
            self.extract()
        

    def scrape(self):
        page = serverRequest.sendRequest(self.url)

        if (page == False):
            return False

        try:
            soup = BeautifulSoup(page.content, "html.parser")
            searchSoup = soup.find(class_ = "daily-update")
            self.soupSearchResults = searchSoup.findAll(href = True)

        except Exception:
            return False

        return True

    def extract(self):
        for i in range(0, len(self.soupSearchResults), 2):
            comicTitle    = self.soupSearchResults[i].text
            latestChapter = self.soupSearchResults[i + 1].text
            menuUrl       = self.soupSearchResults[i]["href"]
            chapUrl       = self.soupSearchResults[i + 1]["href"]
            chapUrl       = chapUrl.split("chapter_")[0] + "chapter_{}"

            if (not menuUrl.startswith("https:")): menuUrl = "https:" + menuUrl
            if (not chapUrl.startswith("https:")): chapUrl = "https:" + chapUrl

            self.append([comicTitle, latestChapter, menuUrl, chapUrl])
