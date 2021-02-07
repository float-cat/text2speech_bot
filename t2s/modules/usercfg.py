from asyncmgr import AsyncMgr
from buffermgr import BufferMgr


class UserCfg(object):
    """Класс UserCfg используется для хранения настроек пользователя

    Основное применение - хранение настроек пользователя в одном месте

    Атрибуты
    --------
    нет

    Методы
    ------
    setSex
    getSex
    setSpeed
    getSpeed
    setLang
    getSex
    setLastAsyncId
    getLastAsyncId
        методы для доступа к приватным полям пользователя
    getAsyncMgr
        возвращает объект менеджера синхронизации пользователя
    getBufferMgr
        возвращает объект менеджера буферизации сообщений пользователя
    """

    def __init__(self):
        self.__sex = "male"
        self.__speed = 1
        self.__dialog = 0
        self.__lang = "ru-RU"
        # Менеджеры синхронизации и буферизации нужны для склеивания
        #   мультисообщений и сообщений разбитых на блоки для асинхронного
        #   приема потока с аудиофайлом сгенерированной речи
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
        """Метод для обработки доступа к пользовательскому менеджеру синхронизации
        Вход: пусто
        Выход: объект класса AsyncMgr (из asyncmgr.py)
        Задача: обеспечить безопасный доступ к менеджеру синхронизации
        """

        return self.__asyncmgr

    def setLastAsyncId(self, asyncid):
        self.__lastasyncid = asyncid

    def getLastAsyncId(self):
        return self.__lastasyncid

    def getBufferMgr(self):
        """Метод для обработки доступа к пользовательскому менеджеру буферизации
        Вход: пусто
        Выход: объект класса BufferMgr (из buffermgr.py)
        Задача: обеспечить безопасный доступ к менеджеру синхронизации
        """

        return self.__buffermgr
