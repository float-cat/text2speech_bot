import requests
from speakers import Speakers


class SpeechKitAdapter(object):
    """Класс SpeechKitAdapter реализует получение аудио от сервиса Yandex SpeechKit

    Основное применение - получение аудио от сервиса YSK

    Атрибуты
    --------
    folder_id
        символьный идентификатор рабочего каталога в сервисах cloud.yandex.ru
    api_key
        символьный идентификатор ключа АПИ для сервисов cloud.yandex.ru
    t2sbot
        объект класса TGText2SpeechBot (из tg_bot.py)

    Методы
    ------
    def synthesize(self, text, userinfo):
        отправляет запрос на синтез речи из переданного текста

    async def getAudio(self, chatid, text, asyncinfo, fileid):
        асинхронное получение аудио
    """

    def __init__(self, folder_id, api_key, t2sbot):
        self.__speakersinfo = Speakers()
        self.__folder_id = folder_id
        self.__api_key = api_key
        self.__t2sbot = t2sbot

    def synthesize(self, text, userinfo):
        """Метод для получения синтезированной речи от сервиса cloud.yandex.ru
        Вход: текст для синтеза, объект UserCfg (из usercfg.py)
        Выход: итерируемый объект
        Задача: синтезироваать речь
        """

        url = "https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize"
        headers = {"Authorization": "Api-Key " + self.__api_key}
        data = {
            "text": text,
            "lang": userinfo.getLang(),
            "folderId": self.__folder_id,
            "speed": userinfo.getSpeed(),
            "voice": self.__speakersinfo.getSpeakerId(userinfo.getLang(), userinfo.getSex()),
        }

        with requests.post(url, headers=headers, data=data, stream=True) as resp:
            if resp.status_code != 200:
                raise RuntimeError("Invalid response received: code: %d, message: %s" % (resp.status_code, resp.text))

            for chunk in resp.iter_content(chunk_size=None):
                yield chunk

    async def getAudio(self, chatid, text, asyncinfo, fileid):
        """Метод для формирования
        Вход: идентификатор чата, текст, набор параметров смещения,
            идентификатор файла
        Выход: пусто
        Задача: сохранить полученное аудио
        """

        asyncid = asyncinfo["asyncid"]
        uniqueid = asyncinfo["uniqueid"]
        offset = asyncinfo["offset"]
        userinfo = self.__t2sbot.getuserinfo(chatid)
        audiofile = "synthesizes/%d_%d_%d.ogg" % (chatid, asyncid, fileid)
        with open(audiofile, "wb") as f:
            try:
                shift = offset + uniqueid
                for audio_content in self.synthesize(text[offset:shift], userinfo):
                    f.write(audio_content)
                f.close()
                userinfo.getAsyncMgr().registerUniqueId(asyncid, uniqueid)
                await self.__t2sbot.onReceivedFile(chatid, asyncid, uniqueid)

            except RuntimeError:
                self.__t2sbot.bot.send_message(chatid, "Похоже что волшебная палочка сломалась :(")
