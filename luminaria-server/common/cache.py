import time


class CachedRequest:
    CACHE_LIMIT = 10
    SECS_TO_EXPIRE = 15

    def __init__(self, app_id, command, data):
        self.start_time = time.time()
        self.app_id = app_id
        self.command = command
        self.data = data
        self.res = None

    def insert(self):
        pass

    def eject(self):
        pass

    def is_expired(self):
        elapsed_time = time.time() - self.start_time
        return elapsed_time >= self.SECS_TO_EXPIRE

    def __eq__(self, other):
        return self.app_id == other.app_id and self.command == other.command and self.data == other.data

    def __hash__(self):
        return hash((self.app_id, self.command, self.data))

