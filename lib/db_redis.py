import redis
import json


class Database(object):
    def __init__(self, host='127.0.0.1', port=6379):
        self.handler = redis.StrictRedis(host=host, port=port, db=0)

    def create(self, prefix, index, data, ttl=None):
        name = '_'.join((prefix, index))
        if self.handler.set(name, json.dumps(data)):
            if ttl is not None:
                self.handler.expire(name, ttl)
            return data
        return False

    def read(self, prefix, index):
        name = '_'.join((prefix, index))
        data = self.handler.get(name)
        if not data:
            return None
        return json.loads(data.decode())

    update = create

    def delete(self, prefix, index):
        name = '_'.join((prefix, index))
        return bool(self.handler.delete(name))

    def exists(self, prefix, index):
        name = '_'.join((prefix, index))
        return bool(self.handler.exists(name))

    def list(self, pattern='*'):
        return [k.decode() for k in self.handler.keys(pattern=pattern)]
