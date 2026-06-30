from collections import deque


class TaskQueue:

    def __init__(self):
        self.queue = deque()

    def add_task(self, task):
        self.queue.append(task)

    def get_task(self):
        if self.queue:
            return self.queue.popleft()

        return None

    def has_tasks(self):
        return len(self.queue) > 0

    def size(self):
        return len(self.queue)

    def clear(self):
        self.queue.clear()
