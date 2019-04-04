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
            searchSoup = soup.find(class_ = "panel_story_list")
            self.soupSearchResults = searchSoup.find_all(class_ = "story_item")
            
        except Exception:
            return False

        return True

    def extract(self):
        for i in range(0, len(self.soupSearchResults), 1):
            c = self.soupSearchResults[i].find(class_ = "story_name").find(href = True)

            comicTitle = c.text
            menuUrl = c["href"]

            if (not menuUrl.startswith("https:")):
                menuUrl = "https:" + menuUrl

            self.append([comicTitle, -1, menuUrl, "N/A"])

            print(self[-1])

