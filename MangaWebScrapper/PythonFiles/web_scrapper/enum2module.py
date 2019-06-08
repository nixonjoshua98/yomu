from enums import WebsiteEnum

from . import (
	manganelo,
	ciayo
)

MODULE_TABLE = {
	WebsiteEnum.MANGANELO: manganelo,
	WebsiteEnum.CIAYO: ciayo
}


def str2module(s):
	if "manganelo" in s:
		return manganelo

	elif "ciayo" in s:
		return ciayo