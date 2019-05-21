class MangaDownloadController:
    from data_structures.queue import Queue

    queue = Queue()

    def __init__(self):
        pass

    def control_loop(self):
        import time

        while True:
            self.queue.append("Hello")

            time.sleep(1)
