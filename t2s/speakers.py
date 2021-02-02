# Speackers names
class Speakers(object):
    def __init__(self):
        self.__speakers = {}
        self.__speakers["female"] = {"Элис": "alyss", "Джейн": "jane", "Оксана": "oksana", "Омаж": "omazh"}
        self.__speakers["male"] = {"Захар": "zahar", "Ермил": "ermil"}

    def getSpeakersBySex(self, sex):
        speakerlist = ""
        for speaker in self.__speakers[sex].keys():
            speakerlist += speaker + " "
        return speakerlist

    def isSpeaker(self, name, sex):
        return name in self.__speakers[sex].keys()

    def getSpeakerId(self, name, sex):
        return self.__speakers[sex][name]
