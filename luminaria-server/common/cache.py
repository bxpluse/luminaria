import time
import random


def hash_tuple(tup):
    temp_lst = []
    for item in tup:
        temp_lst.append(str(item))
    return hash(tuple(temp_lst))


class Cache:
    CACHE_LIMIT = 4

    def __init__(self, secs_to_expire):
        self.cache = {}
        self.SEC_TO_EXPIRE = secs_to_expire

    def fetch(self, hash_id):
        if hash_id in self.cache:
            cached_request = self.cache[hash_id]
            # Eject item if it's expired
            if cached_request.is_expired():
                self.eject(hash_id)
            else:
                # Return saved response
                return cached_request.response
        return None

    def store(self, command, data, response):
        # Eject random item if cache limit reached
        if len(self.cache) > self.CACHE_LIMIT:
            rand_key = random.choice(list(self.cache.keys()))
            self.eject(rand_key)

        # Insert into cache
        cached_request = CachedRequest(command, data, response, self.SEC_TO_EXPIRE)
        hash_id = hash(cached_request)
        self.cache[hash_id] = cached_request

    def eject(self, hash_id):
        del self.cache[hash_id]


class CachedRequest:

    def __init__(self, command, data, response, secs_to_expire):
        self.start_time = time.time()
        self.command = command
        self.data = data
        self.response = response
        self.secs_to_expire = secs_to_expire

    def is_expired(self):
        elapsed_time = time.time() - self.start_time
        return elapsed_time >= self.secs_to_expire

    def __eq__(self, other):
        return self.command == other.command and self.data == other.data

    def __hash__(self):
        tup = (self.command, str(self.data))
        return hash_tuple(tup)
