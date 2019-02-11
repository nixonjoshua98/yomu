#!python3.4

from interface.interface import Interface
from classes.comicDownloadManager import ComicDownloadManager

downloadManager = ComicDownloadManager(10)

Interface(downloadManager).mainloop()
