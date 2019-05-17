from interface.interface import Interface
from classes.comicDownloadManager import ComicDownloadManager

downloadManager = ComicDownloadManager(50)

Interface(downloadManager).mainloop()
 
