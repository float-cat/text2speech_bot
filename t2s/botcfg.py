# Bot Config


class UserCfg(object):
    def __init__(self):
        self.__sex = "male"
        self.__speed = 1
        self.__dialog = 0
        self.__lang = "ru-RU"

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


class BotCfg(object):
    def __init__(self):
        self.__users = {}

    def userInfo(self, chatid):
        if chatid not in self.__users:
            self.__users[chatid] = UserCfg()
        return self.__users[chatid]
