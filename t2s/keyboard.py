# Bot Keyboards structure
from aiogram.types import KeyboardButton
from aiogram.types import ReplyKeyboardMarkup


class BotKeyboard(object):
    def __init__(self):
        self.__speeds = ["x0.5", "x1", "x1.5", "x2"]
        self.__sexs = ["Мужской", "Жeнский"]
        self.__keyboards = {}
        self.__button_speed = KeyboardButton("Скoрость")
        self.__button_speed_cases = []

        for val in self.__speeds:
            self.__button_speed_cases.append(KeyboardButton(val))
        self.__button_sex = KeyboardButton("Пoл М/Ж")
        self.__button_male = KeyboardButton(self.__sexs[0])
        self.__button_female = KeyboardButton(self.__sexs[1])
        self.__keyboards["menu"] = ReplyKeyboardMarkup(resize_keyboard=True)
        self.__keyboards["menu"].row(self.__button_sex, self.__button_speed)
        self.__keyboards["sex"] = ReplyKeyboardMarkup(resize_keyboard=True)
        self.__keyboards["sex"].row(self.__button_male, self.__button_female)
        self.__keyboards["speed"] = ReplyKeyboardMarkup(resize_keyboard=True)
        self.__keyboards["speed"].row(*self.__button_speed_cases)

    def getKeyboardsByState(self, kb):
        if kb in self.__keyboards.keys():
            return self.__keyboards[kb]

        else:
            return self.__keyboards[self.__keyboards.keys()[0]]

    def isSexSetup(self, value):
        return value in self.__sexs

    def isSpeedSetup(self, value):
        return value in self.__speeds
