import redis
from dateutil import parser

REDIS_DB_INDEX = 10

r = redis.Redis(db=REDIS_DB_INDEX, host='localhost', port=6479)


class UserRedisAccess(object):

    REDIS_PREFIX = "user_access"

    def __init__(self, user_id):
        self.user_id = user_id
        self.LAST_ACCESS_KEY = "{0}_{1}_{2}".format(
            self.REDIS_PREFIX,
            self.user_id,
            "last_access"
        )
        self.USER_WAIT_KEY = "{0}_{1}_{2}".format(
            self.REDIS_PREFIX,
            self.user_id,
            "wait"
        )
        super(UserRedisAccess, self).__init__()

    @property
    def last_access(self):
        last_access_date = r.get(self.LAST_ACCESS_KEY)
        if last_access_date is None:
            return None
        else:
            return parser.parse(last_access_date)

    def update_status(self, update_date):
        r.set(self.LAST_ACCESS_KEY, update_date.strftime("%Y-%m-%d %H:%M:%S.%f %Z"))

    def wait(self, wait_date):
        self.update_status(wait_date)
        r.set(self.USER_WAIT_KEY, 1)

    def cancel_wait(self):
        r.delete(self.LAST_ACCESS_KEY)
        r.delete(self.USER)

    @property
    def is_waiting(self):
        if r.get(self.USER_WAIT_KEY) is not None:
            return True
        else:
            return False
