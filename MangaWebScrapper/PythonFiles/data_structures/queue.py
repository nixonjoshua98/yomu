import collections


class Queue(collections.deque):
    def pop(self):
        try:
            val = super().pop()
        except IndexError:
            return None
        else:
            return val