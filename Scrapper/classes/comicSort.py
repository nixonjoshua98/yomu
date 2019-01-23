import data.constants as consts

import operator

class ComicSort:
    pairings = consts.comicSortPairings

    @classmethod
    def textToId(cls, text):
        for i in cls.pairings:
            if (i["text"] == text):
                return i["id"]
        return None

    @classmethod
    def allText(cls):
        return [i["text"] for i in cls.pairings]

    @classmethod
    def sort(cls, data, sortId):
        if (sortId == 0):
            d = cls.sortByComicTitle(data)

        elif (sortId == 1):
            # # # Modified Counting Sort # # #
            countDict   = {}
            sortedData  = []

            for d in data:
                if (not countDict.get(d[-1], False)):
                    countDict[d[-1]] = [d]
                else:
                    countDict[d[-1]].append(d)

            while (len(countDict) > 0):
                key = max(list(countDict.keys()))
                sortedData += sorted(countDict[key])
                countDict.pop(key)
            d = sortedData

        else:
            return data

        return d

    @classmethod
    def sortByComicTitle(cls, data):
        data.sort()
        return data
