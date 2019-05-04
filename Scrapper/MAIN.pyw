from interface.interface import Interface
from classes.comicDownloadManager import ComicDownloadManager

downloadManager = ComicDownloadManager(5)

Interface(downloadManager).mainloop()
 
