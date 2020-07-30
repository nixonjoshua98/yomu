
from src import utils


class _Statuses(type):
	_ALL = (
		dict(id=0, text="Recently Added"),
		dict(id=1, text="Favourites"),
		dict(id=2, text="Reading List"),
		dict(id=3, text="Reading Elsewhere"),
		dict(id=4, text="Dropped"),
		dict(id=5, text="Completed"),
	)

	@property
	def all_text(self):
		return tuple(s["text"] for s in self._ALL)

	def get(self, **kwargs):
		return utils.get(self._ALL, **kwargs)

	def index(self, **kwargs):
		return Statuses._ALL.index(self.get(**kwargs))


class Statuses(metaclass=_Statuses):
	pass
