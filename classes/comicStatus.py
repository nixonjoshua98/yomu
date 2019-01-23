import data.constants as consts

class ComicStatus:
    pairings = consts.comicStatusPairings

    @classmethod
    def textToId(cls, text):
        for i in cls.pairings:
            if (i["text"] == text):
                return i["id"]
        return None

    @classmethod
    def idToDownloadable(cls, id):
        for i in cls.pairings:
            if (i["id"] == id):
                return i["downloadable"]
        return False

    @classmethod
    def allText(cls):
        return [i["text"] for i in cls.pairings]

    @classmethod
    def allViewabaleText(cls):
        return [i["text"] for i in cls.pairings if i.get("viewable", True)]

    @classmethod
    def allId(cls):
        return [i["id"] for i in cls.pairings]
    
