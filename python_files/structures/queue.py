
class Queue:
    ls = []

    def pop(self):
        if len(self.ls) > 0:
            val = self.ls.pop()

            return val

    def append(self, item):
        self.ls.append(item)