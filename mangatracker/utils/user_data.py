import typing
import logging
import configparser

from configparser import ConfigParser


def get(section, key) -> typing.Any:
    config = ConfigParser()

    config.read("mangatracker\\data\\config.ini")

    try:
        return config.get(section, key)
    except configparser.NoSectionError:
        logging.error("Missing config.ini section", exc_info=True)

