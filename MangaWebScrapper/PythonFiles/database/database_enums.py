import enum


class MangaStatusEnum(enum.Enum):
    RECENTLY_ADDED = 0
    FAVOURITES = 1
    READING_LIST = 2
    RARELY_UPDATES = 3
    DROPPED = 4
    COMPLETED = 5

    @property
    def formatted_name(self):
        return self.name.split(".")[-1].title().replace("_", " ")

    @classmethod
    def formatted_name2int(cls, s):
        attr_name = s.upper().replace(" ", "_")

        return getattr(cls, attr_name).value
