from enums import WebsiteEnum

from . import (
	manganelo,
	ciayo
)

MODULE_TABLE = {
	WebsiteEnum.MANGANELO: manganelo,
	WebsiteEnum.CIAYO: ciayo
}

SEARCH_MODULES = {
	WebsiteEnum.MANGANELO: manganelo,
}

# SEARCH_MODULES = MODULE_TABLE


def str2module(s):
	if "manganelo" in s:
		return MODULE_TABLE.get(WebsiteEnum.MANGANELO, None)

	elif "ciayo" in s:
		return MODULE_TABLE.get(WebsiteEnum.CIAYO, None)

	return None
