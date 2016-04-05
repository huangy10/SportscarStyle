import redis


REDIS_DB_INDEX = 10


def incr(key, badge):
    """ increment the badge number
     :param key     the key to access the badge number
     :param badge   the badge number to add

     :return the total badge number
    """
    r = redis.Redis(db=REDIS_DB_INDEX, host='localhost', port=6379)
    return r.incrby(key, badge)


def incr_in_batch(values):
    """ increase the badge number in batch
     :param values key value pair to describe the badge nunber
    """
    r = redis.Redis(db=REDIS_DB_INDEX)
    pipe = r.pipeline()
    badges = dict()
    for (key, badge) in values:
        badges.update(key=pipe.incrby(key, badge))
    pipe.execute()
    return badges


def clear_badge(key):
    r = redis.Redis(db=REDIS_DB_INDEX, host='localhost', port=6379)
    r.delete(key)
