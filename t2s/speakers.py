# Speackers names


def checklanguage(text):

    for char in text.lower():

        if char >= "а" and char <= "я":
            return "ru-RU"

    checknumber = 0
    for char in text:
        if (char >= "0" and char <= "9") or char == " " or char == "-":
            checknumber += 1

    if checknumber == len(text):
        return "ru-RU"

    return "en-US"


class Speakers(object):
    """Класс Speakers используется для организации удобного механизма
    переключения между голосами мужчины и женщины

    Основное применение - вспомогательный механизм для удобства переключения
    различных голосов. Например, если активирован спикер мужчина - русский текст
    будет читать премиум спикер русского языка - Филипп. Английский текст будет
    читать спикер Ник

    Атрибуты
    --------
    пусто

    Методы
    ------
    getSpeakerId
        возвращает идентификатор спикера
    """

    def __init__(self):

        self.__speakers = {}
        self.__speakers["ru-RU"] = {"male": "filipp", "female": "alena"}
        self.__speakers["en-US"] = {"male": "nick", "female": "alyss"}

    def getSpeakerId(self, lang, sex):
        """Метод, который возвращает идентификатор спикера по языку и полу
        Вход: идентификатор языка, пол спикера
        Выход: строковое представление идентификатора спикера
        Задача: получение идентификатораа спикера
        """

        try:
            return self.__speakers[lang][sex]
        except IndexError:
            return self.__speakers["ru-RU"]["male"]
