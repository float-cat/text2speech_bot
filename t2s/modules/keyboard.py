from aiogram.types import KeyboardButton
from aiogram.types import ReplyKeyboardMarkup


class BotKeyboard(object):
    """Класс BotKeyboard используется для формирорования и хранения
    клавиатуры управления ботом

    Основное применение - создание кнопок и клавиатур и их связывание
    в конструкторе класса, затем предоставление доступа к объектам
    соответствующих клавиатур

    Атрибуты
    --------
    пусто

    Методы
    ------
    getKeyboardsByState
        возвращает объект клавиатуры ReplyKeyboardMarkup (aiogram.types)
        соответствующий указанному состоянию (т.е. практически - имени
        клавиатуры). Если клавиатуры для указанного состояния нет, вернет
        первую клавиатуру в списке ключей
    isSexSetup
    isSpeedSetup
        вспомогательные методы для проверки передаваемой строки на вхождение
        в соответствующие списки названий кнопок. Нужны для лаконичной организации
        обработки реакций на нажатие кнопок настройки пола и скорости
    """

    def __init__(self):
        # Заполняем названия кнопок так, чтобы они отличались символьно
        #   от своего вида, т.е., например, в слове Мyжской - y из латинского
        #   алфавита. Это нужно для того, чтобы однозначно отличить сообщение с
        #   кнопки от сообщения из поля ввода сообщений. Иначе на слово Мужской
        #   бот будет срабатывать так, словно нажали соответствующую кнопку
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
        """Метод возвращающий клавиатуру, соответствующую указанному состоянию
        Вход: строковое представление состояния
        Выход: объект клавиатуры ReplyKeyboardMarkup (aiogram.types)
        Задача: организация удобного переключения между клавиатурами
        """

        if kb in self.__keyboards.keys():
            return self.__keyboards[kb]

        else:
            return self.__keyboards[self.__keyboards.keys()[0]]

    def isSexSetup(self, value):
        return value in self.__sexs

    def isSpeedSetup(self, value):
        return value in self.__speeds
