import enum


class EnumWrapper(enum.Enum):
    def prettify(self) -> str:
        return self.name.split(".")[-1].title().replace("_", " ")

    @classmethod
    def str_to_int(cls, enum_string: str) -> int:
        attr_name = enum_string.upper().replace(" ", "_")

        return getattr(cls, attr_name).value


class MangaStatusEnum(EnumWrapper):
    """ Enum class used with the Manga model """

    RECENTLY_ADDED = 0
    FAVOURITES = 1
    READING_LIST = 2
    RARELY_UPDATES = 3
    DROPPED = 4
    COMPLETED = 5

    TESTING = 6
