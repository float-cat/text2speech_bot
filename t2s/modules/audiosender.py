import os

from pydub import AudioSegment


class SenderMgr(object):
    """Класс SenderMgr используется для склеивания частей аудиосообщения
    в одно и отправки этого сообщения пользователю

    Основное применение - склеивание полученных от сервиса распознования
    аудиофайлов в одно цельное сообщение согласно данным менеджера
    асинхронной обработки

    Атрибуты
    --------
    t2sbot
        объект класса TGText2SpeechBot (из tg_bot.py)

    Методы
    ------
    chunksMerge
        объединяет аудиофайлы блоков в один файл
    audioSend
        отправляет объединенный файл пользователю
    """

    def __init__(self, t2sbot):
        self.__t2sbot = t2sbot

    def chunksMerge(self, chatid, asyncid, number):
        """Метод для объединения блоков аудио в один файл
        Вход: идентификатор чата, идентификатор асинхронной обработки
            количество блоков аудио
        Выход: пусто
        Задача: собрать файл из блоков аудио
        """

        audiooutputfile = "synthesizes/%d_%d.ogg" % (chatid, asyncid)
        if number == 1:
            os.rename("synthesizes/%d_%d_0.ogg" % (chatid, asyncid), "synthesizes/%d_%d.ogg" % (chatid, asyncid))
            return
        audiofile1 = "synthesizes/%d_%d_0.ogg" % (chatid, asyncid)
        audiofile2 = "synthesizes/%d_%d_1.ogg" % (chatid, asyncid)
        filecontent1 = AudioSegment.from_ogg(audiofile1)
        filecontent2 = AudioSegment.from_ogg(audiofile2)
        os.remove(audiofile1)
        os.remove(audiofile2)
        outputfile = filecontent1 + filecontent2
        for i in range(2, number):
            audiofile = "synthesizes/%d_%d_%d.ogg" % (chatid, asyncid, i)
            inputfile = AudioSegment.from_ogg(audiofile)
            outputfile += inputfile
            os.remove(audiofile)
        outputfile.export(audiooutputfile, format="ogg", codec="libopus")

    async def audioSend(self, chatid, asyncid):
        """Метод для отправки объединеного файла пользователю
        Вход: идентификатор чата, идентификатор асинхронной обработки
        Выход: пусто
        Задача: собрать файл из блоков аудио
        """

        audiofile = "synthesizes/%d_%d.ogg" % (chatid, asyncid)
        f = open(audiofile, "rb")
        await self.__t2sbot.bot.send_voice(chatid, f)
        f.close()
        os.remove(audiofile)
