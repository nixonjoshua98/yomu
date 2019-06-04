import os
import webbrowser
import subprocess

import resources.constants as constants

import functions.helper_functions as helper_functions


def callback_once_true(master, attr, search_obj, callback):
    if getattr(search_obj, attr):
        callback()
    else:
        master.after(100, callback_once_true, master, attr, search_obj, callback)


def get_latest_offline_chapter(title: str) -> float or int:
    manga_dir = os.path.join(constants.MANGA_DIR, title)

    if os.path.isdir(manga_dir):
        files = os.listdir(manga_dir)

        return max(map(lambda f: functions.remove_trailing_zeros_if_zero(f.split()[-1].replace(".pdf", "")), files))
    return 0


def open_manga_in_explorer(title):
    path = os.path.join(constants.MANGA_DIR, functions.remove_nasty_chars(title))

    subprocess.call("explorer {}".format(path, shell=True))


def open_manga_in_browser(url):
    webbrowser.open(url, new=False)
