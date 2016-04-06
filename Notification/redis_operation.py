import redis

REDIS_DB_INDEX = 10
r = redis.Redis(db=REDIS_DB_INDEX, host='localhost', port=6379)


def incr_notif(key, badge):
    notif_num = r.incrby("notif:{}".format(key), badge)
    chat_num = r.get("chat:{}".format(key))
    if chat_num is None:
        chat_num = 0
    else:
        chat_num = int(chat_num)
    return notif_num + chat_num


def incr_chat(key, badge):
    chat_num = r.incrby("chat:{}".format(key), badge)
    notif_num = r.get("notif:{}".format(key))
    if notif_num is None:
        notif_num = 0
    else:
        notif_num = int(notif_num)
    return chat_num + notif_num


def clear_notif(key):
    r.delete("notif:{}".format(key))
    chat_num = r.get("chat:{}".format(key))
    if chat_num is None:
        chat_num = 0
    else:
        chat_num = int(chat_num)
    return chat_num


