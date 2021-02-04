# User config
from asyncmgr import AsyncMgr


class UserCfg(object):
    def __init__(self):
        self.__sex = "male"
        self.__speed = 1
        self.__dialog = 0
        self.__lang = "ru-RU"
        self.__asyncmgr = AsyncMgr()

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

    def asyncid(self):
        self.__asyncid = (self.__asyncid + 1) % 100
        return self.__asyncid
