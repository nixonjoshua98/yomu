import dataclasses as dc


@dc.dataclass(frozen=True)
class Status:
    id: int
    display_text: str


class StatusListMeta(type):
    _ALL = (
        Status(id=0, display_text="Recently Added"),
        Status(id=2, display_text="Reading List"),
        Status(id=4, display_text="Dropped"),
        Status(id=5, display_text="Completed"),
    )

    def get_by_id(cls, id_):
        return next(x for x in cls._ALL if x.id == id_)

    def __iter__(self):
        return iter(self._ALL)


class StatusList(type, metaclass=StatusListMeta):
    ...

