import functions
import tempfile
import os

from reportlab.pdfgen import canvas


class DownloadBase:
	def __init__(self, src_url, dst_path):
		self.image_urls = []

		self.src_url = src_url
		self.dst_path = dst_path
		self.image_save_paths = []
		self.success = False

	def start(self):
		self.get_image_urls()

		if len(self.image_urls) > 0:
			with tempfile.TemporaryDirectory() as temp_dir:
				self.download_image_urls(temp_dir)
				self.create_pdf()

	def get_image_urls(self): ...

	def download_image_urls(self, temp_save_dir):
		for i, image_url in enumerate(self.image_urls):
			image_ext = image_url.split(".")[-1]
			image_dst_path = os.path.join(temp_save_dir, f"{i}.{image_ext}")

			if functions.copy_file_url_to_file(image_url, image_dst_path):
				self.image_save_paths.append(image_dst_path)

	def create_pdf(self):
		pdf = canvas.Canvas(self.dst_path)

		for image in self.image_save_paths:
			image_size = functions.get_image_dimensions(image)

			if image_size is not None:
				pdf.setPageSize((image_size.width, image_size.height))
				pdf.drawImage(image, x=0, y=0)
				pdf.showPage()
		try:
			pdf.save()

		except Exception:
			pass

		else:
			self.success = True

