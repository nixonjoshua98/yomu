
class Queue:
    ls = []

    def pop(self):
        if len(self.ls) > 0:
            val = self.ls.pop(0)

            return val

    def append(self, item):
        self.ls.append(item)