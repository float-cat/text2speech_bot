from speakers import Speakers
# Bot Config
# Dialog processing status
gd_status = {
    'normal': 0,
    'wait_speaker': 1,
    'wait_speed': 2
}
speakersinfo = Speakers()


class UserCfg(object):
    def __init__(self):
        self.__sex = 'male'
        self.__voice = 'zahar'
        self.__speed = 1
        self.__dialog = 0
        self.__lang = 'ru-RU'

    def setSex(self, value):
        self.__sex = value

    def getSex(self):
        return self.__sex

    def setVoice(self, value, sex):
        self.__voice = speakersinfo.getSpeakerId(value, sex)

    def getVoice(self):
        return self.__voice

    def setSpeed(self, value):
        self.__speed = value

    def getSpeed(self):
        return self.__speed

    def setDialog(self, value):
        self.__dialog = gd_status[value]

    def checkDialog(self, value):
        return self.__dialog == gd_status[value]

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
