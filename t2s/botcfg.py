# Bot Config
from usercfg import UserCfg


class BotCfg(object):
    def __init__(self):
        self.__users = {}

    def userInfo(self, chatid):
        if chatid not in self.__users:
            self.__users[chatid] = UserCfg()
        return self.__users[chatid]
