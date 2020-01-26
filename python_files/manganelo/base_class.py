import requests
import shutil
import dataclasses
import typing

from PIL import Image


@dataclasses.dataclass()
class Rect:
	w: int
	h: int


class BaseClass:
	@staticmethod
	def _send_request(url):
		headers = requests.utils.default_headers()

		page = requests.get(url, stream=True, timeout=5, headers=headers)

		if page.status_code == requests.codes.ok:
			return page

		else:
			return None

	@classmethod
	def _download_url(cls, src: str, dst: str) -> bool:
		image_file = cls._send_request(src)

		is_ok = True

		if image_file:
			with open(dst, "wb") as f:
				image_file.raw.decode_content = True

				try:
					shutil.copyfileobj(image_file.raw, f)

				except:
					is_ok = False

		return is_ok

	@staticmethod
	def _get_image_size(path: str) -> typing.Union[Rect, None]:
		try:
			with Image.open(path) as img:
				rect = Rect(*img.size)

		except (OSError, UnboundLocalError):
			return None

		return rect
