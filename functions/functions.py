import os
import subprocess

import data.constants as consts

def formatName(string):
    return "".join([i for i in string if i not in ':\\/|*"><?.,'])

def removeNastyChars(s):
    return s.replace("–", "-")

def parseToNumber(s):
    try:
        float(s)

    except ValueError as e:
        return str(s)

    else:
        if ("." in str(s)):
            return float(s)
        else:
            return int(s)

def getAvailableChaps(comicTitle, latestChapRead):
    comicTitle     = formatName(comicTitle)
    latestChapRead = parseToNumber(latestChapRead)
    
    if (isinstance(latestChapRead, str)):
        return 0
    
    path = os.path.join(consts.comicOutputDir, comicTitle)

    if (os.path.isdir(path)):
        files = os.listdir(path)
        for i in range(0, len(files)):
            f = parseToNumber(files[i].split()[-1].replace(".pdf", ""))
            files[i] = f

        if (latestChapRead == 0):
            return len(files)

        elif (latestChapRead in files):
            files.sort()
            _id = files.index(latestChapRead)
            return max(len(files[_id + 1:]), 0)
        
    return 0

def openComicInExplorer(comicTitle):
    path = os.path.join(consts.comicOutputDir, formatName(comicTitle))
    subprocess.call("explorer {}".format(path, shell = True))

def getLatestChapter(comicTitle):
    comicTitle = formatName(comicTitle)
    path       = os.path.join(consts.comicOutputDir, comicTitle)

    if (os.path.isdir(path)):
        files = os.listdir(path)
        for i in range(0, len(files)):
            f = parseToNumber(files[i].split()[-1].replace(".pdf", ""))
            files[i] = f
        return max(files)
    return 0
