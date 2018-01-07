import random
import string

from lib.db_redis import Database


PREFIX = ''.join(
    random.choice(string.ascii_lowercase + string.digits) for _ in range(8)
)
DB = Database(host='127.0.0.1', port=6379)
