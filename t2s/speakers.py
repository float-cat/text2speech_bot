# Speackers names


def checklanguage(text):
    rus = 0
    eng = 0
    for char in text.lower():
        if char >= "а" and char <= "я":
            rus += 1
        elif char >= "a" and char <= "z":
            eng += 1
    if eng < rus:
        return "ru-RU"
    else:
        return "en-US"


class Speakers(object):
    def __init__(self):
        self.__speakers = {}
        self.__speakers["ru-RU"] = {"male": "filipp", "female": "alena"}
        self.__speakers["en-US"] = {"male": "nick", "female": "alyss"}

    def getSpeakerId(self, lang, sex):
        return self.__speakers[lang][sex]
