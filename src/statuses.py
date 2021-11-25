import dataclasses

from src import utils


@dataclasses.dataclass(frozen=True)
class Status:
    id: int
    display_text: str


class StatusListMeta(type):
    _ALL = (
        Status(id=0, display_text="Recently Added"),
        Status(id=1, display_text="Favourites"),
        Status(id=2, display_text="Reading List"),
        Status(id=4, display_text="Dropped"),
        Status(id=5, display_text="Completed"),
    )

    def get_by_id(cls, id_):
        return utils.get(cls._ALL, id=id_)

    def __iter__(self):
        return iter(self._ALL)


class StatusList(type, metaclass=StatusListMeta):
    ...
