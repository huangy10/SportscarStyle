import redis

REDIS_DB_INDEX = 10
r = redis.Redis(db=REDIS_DB_INDEX, host='localhost', port=6379)

class UnreadUtil(object):

    r = redis.Redis(db=REDIS_DB_INDEX, host='localhost', port=6379)

    @classmethod
    def incr(cls, key):
        """
        :param key: id of the user
        :return:
        """
        key = "unread:{}".format(key)
        return r.incr(key)

    @classmethod
    def get(cls, key):
        key = "unread:{}".format(key)
        return r.get(key)

    @classmethod
    def clear(cls, key):
        key = "unread:{}".format(key)
        r.delete(key)

    @classmethod
    def set(cls, key, badge):
        cur = cls.get(key)
        if badge < cur:
            cls._set(key, badge)

    @classmethod
    def _set(cls, key, value):
        key = "unread:{}".format(key)
        r.set(key, value)
