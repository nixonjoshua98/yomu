import enum


class EnumWrapper(enum.Enum):
    def prettify(self) -> str:
        return self.name.split(".")[-1].title().replace("_", " ")

    @classmethod
    def all_prettify(cls):
        return [e.prettify() for e in cls]

    @classmethod
    def str_to_int(cls, enum_string: str) -> int:
        attr_name = enum_string.upper().replace(" ", "_")

        return getattr(cls, attr_name).value

    @classmethod
    def get_index(cls, val):
        _enum = MangaStatusEnum(val)

        for i, e in enumerate(MangaStatusEnum):
            if e == _enum:
                return i
        return -1


class MangaStatusEnum(EnumWrapper):
    """ Enum class used with the Manga model """

    RECENTLY_ADDED = 0
    FAVOURITES = 1
    READING_LIST = 2
    READING_ELSEWHERE = 3
    DROPPED = 4
    COMPLETED = 5

    TEST = 6


class WebsiteEnum:
    MANGANELO = 0
