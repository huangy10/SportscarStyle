import redis


REDIS_DB_INDEX = 9
r = redis.Redis(db=REDIS_DB_INDEX, host='localhost', port=6379)


class ChatRemarkNameStorage(object):

    @classmethod
    def get_redis_key(cls, host, user):
        redis_key = "remark_name:{0}_{1}".format(host.id, user.id)
        return redis_key

    @classmethod
    def set_nick_name(cls, host, user, name):
        if host.id == user.id:
            return
        redis_key = cls.get_redis_key(host, user)
        if name is None or name == user.nick_name:
            # if the name to be set is None, treat it as deletion request
            # if the name to be set is exactly the same with the target user's name, delete the record as well to save
            # storage space
            r.delete(redis_key)
        else:
            r.set(redis_key, name)

    @classmethod
    def get_nick_name(cls, host, user):
        if host.id == user.id:
            return user.nick_name
        redis_key = cls.get_redis_key(host, user)
        name = r.get(redis_key)
        if name is None:
            return user.nick_name
        else:
            return name.decode("utf8")


class UnreadMessageNumStorage(object):

    @classmethod
    def get_redis_key(cls, host):
        redis_key = "unread_num:{0}".format(host.id)
        return redis_key

    @classmethod
    def set_unread_num(cls, user, num):
        redis_key = cls.get_redis_key(user)
        r.set(redis_key, num)

    @classmethod
    def incr_unread_num(cls, user):
        redis_key = cls.get_redis_key(user)
        unread = r.incr(redis_key)
        return int(unread)

    @classmethod
    def clear_unread_num(cls, user):
        cls.set_unread_num(user, 0)

