# User config
from asyncmgr import AsyncMgr
from buffermgr import BufferMgr


class UserCfg(object):
    def __init__(self):
        self.__sex = "male"
        self.__speed = 1
        self.__dialog = 0
        self.__lang = "ru-RU"
        self.__asyncmgr = AsyncMgr()
        self.__buffermgr = BufferMgr()
        self.__lastasyncid = -1

    def setSex(self, value):
        self.__sex = value

    def getSex(self):
        return self.__sex

    def setSpeed(self, value):
        self.__speed = value

    def getSpeed(self):
        return self.__speed

    def setLang(self, value):
        self.__lang = value

    def getLang(self):
        return self.__lang

    def getAsyncMgr(self):
        return self.__asyncmgr

    def setLastAsyncId(self, asyncid):
        self.__lastasyncid = asyncid

    def getLastAsyncId(self):
        return self.__lastasyncid

    def getBufferMgr(self):
        return self.__buffermgr
