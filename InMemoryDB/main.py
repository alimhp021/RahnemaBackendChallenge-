import re
import time
import random
from collections import OrderedDict, defaultdict

class Database:
    def __init__(self, name, max_size=10, eviction_policy="random"):
        self.name = name
        self.max_size = max_size
        self.eviction_policy = eviction_policy
        self.data = {}
        self.ttl = {}
        self.access_order = OrderedDict()

    def _evict(self):
        if self.eviction_policy == "random":
            key_to_evict = random.choice(list(self.data.keys()))
            self.delete(key_to_evict)
        elif self.eviction_policy == "noeviction":
            raise Exception("Database is full. Cannot add new key.")
        elif self.eviction_policy == "lru":
            key_to_evict = next(iter(self.access_order))
            self.delete(key_to_evict)

    def set(self, key, value, ttl=None):
        if len(self.data) >= self.max_size and key not in self.data:
            self._evict()

        self.data[key] = value
        if ttl:
            self.ttl[key] = time.time() + ttl
        elif key in self.ttl:
            del self.ttl[key]

        if self.eviction_policy == "lru":
            if key in self.access_order:
                del self.access_order[key]
            self.access_order[key] = None

        return "ok"

    def get(self, key):
        if key in self.ttl and time.time() > self.ttl[key]:
            self.delete(key)
            return "null"

        if key in self.data:
            if self.eviction_policy == "lru":
                if key in self.access_order:
                    del self.access_order[key]
                self.access_order[key] = None
            return self.data[key]
        else:
            return "null"

    def delete(self, key):
        if key in self.data:
            del self.data[key]
            if key in self.ttl:
                del self.ttl[key]
            if key in self.access_order:
                del self.access_order[key]
            return "true"
        else:
            return "false"

    def keys(self, pattern, page=1, limit=10):
        regex = re.compile(pattern)
        matched_keys = [key for key in self.data.keys() if regex.match(key)]
        start = (page - 1) * limit
        return matched_keys[start:start + limit]


class InMemoryDatabase:
    def __init__(self):
        self.databases = {}
        self.current_db = "default"
        self.databases[self.current_db] = Database(self.current_db)

    def execute(self, command):
        parts = command.split()
        cmd = parts[0]

        if cmd == "set":
            key = parts[1]
            value = parts[2]
            ttl = int(parts[3]) if len(parts) > 3 else None
            return self.databases[self.current_db].set(key, value, ttl)

        elif cmd == "get":
            key = parts[1]
            return self.databases[self.current_db].get(key)

        elif cmd == "del":
            key = parts[1]
            return self.databases[self.current_db].delete(key)

        elif cmd == "keys":
            pattern = parts[1]
            page = int(parts[3]) if len(parts) > 3 else 1
            limit = int(parts[5]) if len(parts) > 5 else 10
            return self.databases[self.current_db].keys(pattern, page, limit)

        elif cmd == "use":
            db_name = parts[1]
            max_size = int(parts[2]) if len(parts) > 2 else 10
            eviction_policy = parts[3] if len(parts) > 3 else "random"
            if db_name not in self.databases:
                self.databases[db_name] = Database(db_name, max_size, eviction_policy)
            self.current_db = db_name
            return "db switched"

        elif cmd == "list":
            return list(self.databases.keys())

        elif cmd == "exit":
            exit(0)

        else:
            return "unknown command"

if __name__ == "__main__":
    db = InMemoryDatabase()
    while True:
        command = input()
        output = db.execute(command)
        print(output)
