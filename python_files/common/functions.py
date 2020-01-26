import typing
import os

from python_files.common import constants


def remove_trailing_zeroes(s: str) -> typing.Union[int, float]:
	s = str(s)

	return int(s) if s.count(".") == 0 or s.endswith(".0") else float(s)


def remove_nasty_chars(s) -> str:
	try:
		return "".join([i for i in s if i not in ':\\/|*"><?.,'])
	except TypeError:
		return s


def get_manga_save_dir(manga_title, chapter) -> str:
	output_dir = os.path.join(constants.MANGA_DIR, manga_title)
	file_name = f"{manga_title} Chapter {chapter}.pdf"

	return os.path.join(output_dir, file_name)