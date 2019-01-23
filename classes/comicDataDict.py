class ComicDataDict(dict):
    def keyExists(self, key):
        return key in self.keys()

    def updateKey(self, k, v):
        self[k] = v

    def getValue(self, k):
        return self[k]
