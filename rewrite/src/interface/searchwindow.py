from . import (Toplevel)


class SearchWindow(Toplevel):
    def __init__(self,):
        super(SearchWindow, self).__init__("Search Results")

        self.center_in_root()
