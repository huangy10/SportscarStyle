import json
from redisco.containers import List


class MessageList(List):
    def __init__(self, key, db=None, pipeline=None, capacity=128):
        self.capacity = capacity
        super(MessageList, self).__init__(key, db, pipeline)

    def append(self, value):
        if len(self) >= self.capacity:
            self.shift()
        super(MessageList, self).append(value)

    def unshift(self, value):
        if len(self) >= self.capacity:
            self.pop()
        super(MessageList, self).unshift(value=value)

    def pack_to_json(self, clear_after_pack=True):
        """
        Pack the cached messages into serialized response json object
        :param clear_after_pack: if True, the data in redis will be cleared before return
        :return:
        """
        data = self.members
        if len(data) == 0:
            return []
        data = map(lambda x: json.loads(x), data)
        if clear_after_pack:
            self.clear()
        return data


