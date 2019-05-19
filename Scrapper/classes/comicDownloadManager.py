import random
import time
import os
import threading

# Static class
from classes.database import Database

import data.constants      as consts
import functions.functions as funcs

from manganelo.chapterList     import ChapterList
from manganelo.downloadChapter import DownloadChapter

class ComicDownloadManager():
    def __init__(self, maxThreads):
        self.active     = True
        self.maxThreads = maxThreads
        self.queue      = []
        self.threadsRunning = 0
        self.recordsCount   = 0
        self.idsDownloading = []
        self.comicDataGen   = self.comicDataGen()

        threading.Thread(target = self.controller).start()

    def stop(self):
        self.active = False

    def comicDataGen(self):
        while (self.active):
            #data = Database.getAllDownloadableComics()
            data = Database.getDownloadableComics()
            random.shuffle(data)
            self.recordsCount = len(data)

            for c in data:
                yield c
                
    def controller(self):
        while (self.active):
            threadAvailable = self.maxThreads - self.threadsRunning >= 1
            currentThreadsAreEnough = False

            if (self.threadsRunning > 0): 
                currentThreadsAreEnough = (self.recordsCount / self.threadsRunning) < 10

            if (threadAvailable and not currentThreadsAreEnough):
                rawData = next(self.comicDataGen)
                data = {"comicId": rawData[0], "comicTitle": rawData[1], "menuUrl": rawData[2]}

                if (data["comicId"] not in self.idsDownloading):
                    threading.Thread(target = self.downloader, args = (data,)).start()
                    self.threadsRunning += 1

            time.sleep(1.5)

    def downloader(self, comicData):
        self.idsDownloading.append(comicData["comicId"])

        chapterList = ChapterList(comicData["menuUrl"])
        
        for c in chapterList:
            chapUrl = c[0]
            chapNum = c[1]

            formattedComicTitle = funcs.formatName(comicData["comicTitle"])

            outputDir = os.path.join(consts.comicOutputDir, formattedComicTitle)
            fileName = "{0} Chapter {1}.pdf".format(formattedComicTitle, chapNum)

            os.makedirs(outputDir, exist_ok = True)

            if (not os.path.isfile(os.path.join(outputDir, fileName))):
                chapterDownload = DownloadChapter(chapUrl, outputDir, fileName)

                if (chapterDownload.success):
                    print(chapUrl, comicData["comicTitle"], chapNum, sep = " | ")
                    self.queue.append([comicData["comicTitle"], "Chapter {0}".format(chapNum)])

        self.idsDownloading.pop(self.idsDownloading.index(comicData["comicId"]))
        self.threadsRunning -= 1




