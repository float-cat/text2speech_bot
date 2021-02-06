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
    def __init__(self):

        self.__speakers = {}
        self.__speakers["ru-RU"] = {"male": "filipp", "female": "alena"}
        self.__speakers["en-US"] = {"male": "nick", "female": "alyss"}

    def getSpeakerId(self, lang, sex):

        return self.__speakers[lang][sex]
