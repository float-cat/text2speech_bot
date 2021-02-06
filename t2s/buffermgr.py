# Buffer of multimessage

class BufferMsg(object):
    def __init__(self, uniqueids, msg):
        self.__uniqueids = uniqueids
        self.__buffer = msg

    def getUniqueIds(self):
        return self.__uniqueids

    def getMsg(self):
        return self.__buffer


class BufferMultiMsg(object):
    def __init__(self):
        self.__buffer = []

    def pushMsg(self, uniqueids, msg):
        self.__buffer.append(BufferMsg(uniqueids, msg))

    def numberMessages(self):
        return len(self.__buffer)

    def getMessage(self, msgid):
        return self.__buffer[msgid]

    def clear(self):
        self.__buffer.clear()


class BufferMgr(object):
    def __init__(self):
        self.__tmpasyncid = -1
        self.__buffer = []

    def pushMsg(self, asyncid, uniqueids, msg):
        if self.__tmpasyncid < asyncid:
            self.__buffer.append(BufferMultiMsg())
            self.__tmpasyncid = asyncid
        self.__buffer[asyncid].pushMsg(uniqueids, msg)

    def getMultiMsg(self, asyncid):
        return self.__buffer[asyncid]

    def delMsg(self, asyncid):
        self.__buffer[asyncid].clear()
