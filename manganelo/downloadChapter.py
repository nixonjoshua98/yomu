from bs4              import BeautifulSoup
from reportlab.pdfgen import canvas

import PIL
import tempfile
import os
import shutil
import urllib

import functions.serverRequest as serverRequest

class DownloadChapter(object):
    def __init__(self, chapUrl, outDir, fileName):
        self.chapUrl    = chapUrl
        self.success    = False
        self.imageUrls  = []
        self.imagePaths = []
        self.fullOutputPath = os.path.join(outDir, fileName)

        self.imageSaveDir = tempfile.mkdtemp()

        if (self.scrape()):
            if (self.downloadImages()):
                self.createChapter()

        shutil.rmtree(self.imageSaveDir, ignore_errors = True)

    def scrape(self):
        page = serverRequest.sendRequest(self.chapUrl)

        if (page == False):
            return False


        try:
            soup = BeautifulSoup(page.content, "html.parser")
            
            imageSoup = soup.findAll("img")

        except Exception:
            """ Error occurred when attempting to scrape images """
            return False

        else:
            self.imageUrls = [i["src"] for i in imageSoup]
            return True

    def downloadImages(self):
        for i, imgUrl in enumerate(self.imageUrls):
            imgExtension = imgUrl.split(".")[-1]
            imgPath = os.path.join(self.imageSaveDir, "{0}.{1}".format(i, imgExtension))
            
            img = serverRequest.sendRequest(imgUrl)

            if (img == False):
                continue

            with open(imgPath, "wb") as f:
                img.raw.decode_content = True
                try:
                    shutil.copyfileobj(img.raw, f)
                except Exception:
                    """ Most likely timeout error """
                else:
                    self.imagePaths.append(imgPath)

        return len(self.imagePaths) > 0

    def createChapter(self):
        pdf = canvas.Canvas(self.fullOutputPath)
        for img in self.imagePaths:
            try:
                with PIL.Image.open(img) as i:
                    w, h = i.size
            except OSError as e: # Image file was not downloaded correctly
                continue

            pdf.setPageSize((w, h))
            pdf.drawImage(img, x = 0, y = 0)
            pdf.showPage()

        try:
            pdf.save()

        except Exception:
            """ Could not save the pdf for an unknown reason """

        else:
            self.success = True
