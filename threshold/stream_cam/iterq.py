from multiprocessing import Process, Queue, Pool
import queue

class IterQueue(queue.Queue):

    def __init__(self):
        super().__init__()
        self.current = 0
        self.end = self.current +1

    def __iter__(self):
        self.current = 0
        self.end = 10000
        while True:
            yield self.get()

    def __next__(self):
        if self.current >= self.end:
            raise StopIteration
        current = self.current
        self.current += 1
        return current
