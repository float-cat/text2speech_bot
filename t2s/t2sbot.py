import asyncio
import logging
import os
import sys

from aiogram import Bot
from aiogram import Dispatcher
from aiogram import executor
from aiogram import types

sys.path.insert(0, "modules")

from asyncmgr import MERGE_TIMEOUT  # noqa: E402
from asyncmgr import WAIT_MORE  # noqa: E402
from audiosender import SenderMgr  # noqa: E402
from botcfg import BotCfg  # noqa: E402
from keyboard import BotKeyboard  # noqa: E402
from preprocessing import TextPreprocessing  # noqa: E402
from speakers import checklanguage  # noqa: E402
from speechkitadapter import SpeechKitAdapter  # noqa: E402

MAX_LEN_SEGMENT = 500

# Enviropment variables
env_config = {}
env_config["API_TOKEN"] = os.environ.get("GLOBAL_TG_TOKEN")
env_config["API_KEY"] = os.environ.get("GLOBAL_API_KEY")
env_config["ID_FOLDER"] = os.environ.get("GLOBAL_ID_FOLDER")


class TGText2SpeechBot(object):
    """Класс TGText2SpeechBot реализует основную работу программы

    Основное применение - это главный класс проекта, класс описывает
    логику бота

    Атрибуты
    --------
    env_config
        словарь с необходимыми переменными окружения, такими как токен бота или ключ API

    Методы
    ------
    getuserinfo
        получение информации о пользователе
    show_welcome
        сообщение приветствия
    change_sex
        смена спикера на спикера другого пола
    change_speed
        смена скорости
    askt2s_service
        асинхронная задача для запуска асинхронного скачивания
    do_echo
        обработчик сообщений от пользователя
    onReceivedFile
        функция обратного вызова для проверки завершения приема данных
    """

    def __init__(self, env_config):

        self.bot = Bot(token=env_config["API_TOKEN"])
        self.dp = Dispatcher(self.bot)
        self.__keyboard = BotKeyboard()

        self.__botcfg = BotCfg()
        self.__text2speechAdapter = SpeechKitAdapter(env_config["ID_FOLDER"], env_config["API_KEY"], self)
        self.__sendermgr = SenderMgr(self)

    def getuserinfo(self, chatid):

        return self.__botcfg.userInfo(chatid)

    async def show_welcome(self, message):

        await self.bot.send_message(
            message.chat.id,
            "Привет, " + message.from_user.first_name + "!",
            reply_markup=self.__keyboard.getKeyboardsByState("menu"),
        )

    async def change_sex(self, message, userinfo):

        if message.text == "Жeнский":
            userinfo.setSex("female")
        else:
            userinfo.setSex("male")

        await self.bot.send_message(
            message.chat.id,
            "Пол голоса был изменен на " + message.text.lower(),
            reply_markup=self.__keyboard.getKeyboardsByState("menu"),
        )

    async def change_speed(self, message, userinfo):

        speedsetup = float(message.text[1:])
        userinfo.setSpeed(speedsetup)

        await self.bot.send_message(
            message.chat.id, f"Скорость теперь {speedsetup}", reply_markup=self.__keyboard.getKeyboardsByState("menu")
        )

    async def askt2s_service(self, chatid, asyncid):
        """Метод асинхронного запроса к серверу преобразования текст в голос
        Вход: идентификатор чата, идентификатор асинхронной обработки
        Выход: пусто
        Задача: запустить несколько асинхронных задач для скачивания результатов
        Примечание: Должна запускаться как асинхронная задача
        """

        # Вызываем асинхронный вариант sleep
        await asyncio.sleep(MERGE_TIMEOUT)
        # Используем дополнительные переменные для более коротого кода
        userinfo = self.getuserinfo(chatid)
        multimsg = userinfo.getBufferMgr().getMultiMsg(asyncid)
        # Переменная отслеживает одномерный индекс для двухмерного цикла
        indexofsegment = 0

        # Цикл обработки сообщений из мультисообщения (BufferMultiMsg)
        for i in range(0, multimsg.numberMessages()):
            uniqueids = multimsg.getMessage(i).getUniqueIds()
            text = multimsg.getMessage(i).getMsg()
            # Переменная отслеживает смещение блока в сообщении
            startsegment = 0
            # Цикл обработки одинарного сообщения.
            #   Разбивает на блоки и создает асинхронную задачу получения аудио
            for j in range(0, len(uniqueids)):
                # Переменная отслеживает дополнение смещения
                shift = startsegment

                # Если блок не первый (уже есть смещение) - то добавляем 1
                #   тем самым мы исключаем пробел
                if startsegment > 0:
                    shift += 1

                # Заполняем словарь параметрами, служит для сокращения числа аргументов функции
                asyncinfo = {"asyncid": asyncid, "uniqueid": uniqueids[j], "offset": shift}
                # Запускаем асинхронную задачу
                asyncio.create_task(self.__text2speechAdapter.getAudio(chatid, text, asyncinfo, indexofsegment + j))
                # отслеживаем смещение следующего блока
                startsegment += uniqueids[j]

            # Отслеживаем одномерный индекс, добавляя колво индексов одинарного сообщения
            indexofsegment += len(uniqueids)

    async def do_echo(self, message):
        """Метод обрабатывает принятые сообщения от бота
        Вход: объект сообщения из библиотеки aiogram
        Выход: пусто (в теле метода есть явный вызов пустого возврата)
        Задача: обработать сообщения пользовтеля, организовать обработку кнопок - т.к.
            кнопки клавиатуры типа reply - это кнопки, которые просто отсылают в чат
            свое название как сообщение
        """

        userinfo = self.getuserinfo(message.chat.id)

        if message.text == "Пoл М/Ж":

            await self.bot.send_message(
                message.chat.id, "Выберите пол", reply_markup=self.__keyboard.getKeyboardsByState("sex")
            )

            return

        elif self.__keyboard.isSexSetup(message.text):
            await self.change_sex(message, userinfo)

            return

        elif message.text == "Скoрость":
            await self.bot.send_message(
                message.chat.id,
                "Выберите скорость из списка доступных",
                reply_markup=self.__keyboard.getKeyboardsByState("speed"),
            )

            return

        elif self.__keyboard.isSpeedSetup(message.text):

            await self.change_speed(message, userinfo)

            return

        # Вызываем предобработку текста, чтобы исключить теги и ссылки
        text = TextPreprocessing(message.text)

        # Если после предобработки текст остался пустым - уходим
        if len(text) < 1:
            return

        userinfo.setLang(checklanguage(text))
        # Получаем идентификатор асинхронной обработки
        asyncid = userinfo.getAsyncMgr().getAsyncId()

        # Если полученый идентификатор отличается от последнего
        #   значит таймаут склеивания сообщений истек, поступило
        #   отдельное сообщение
        if userinfo.getLastAsyncId() != asyncid:
            await self.bot.send_message(message.chat.id, "Происходит магия...")
            # обновляем последний идентификатор асинхронной обработки, чтобы
            #   начать склеивать сообщения
            userinfo.setLastAsyncId(asyncid)
            # Запукаем задачу асинхронной обработки
            #   функция после входа засыпает, чтобы
            #   было время склеить сообщения
            asyncio.create_task(self.askt2s_service(message.chat.id, asyncid))

        # Подготавливаем уникальные идентификаторы блоков сообщений
        uniqueids = userinfo.getAsyncMgr().genUniqueIdsFree(message.text, MAX_LEN_SEGMENT)
        # Регистрируем дополнительное количество блоков, ожидающих прием
        userinfo.getAsyncMgr().registerChunksNumber(asyncid, len(uniqueids))
        # Размещаем сообщение в буфере
        userinfo.getBufferMgr().pushMsg(asyncid, uniqueids, message.text)

    async def onReceivedFile(self, chatid, asyncid, uniqueid):
        """Метод обратной связи (callback). Передается не сам, а self этого класса
        Вход: идентификатор чата, идентификатор асинхронной обработки, уникальный идентификатор блока
        Выход: пусто
        Задача: Зарегистрировать прием сообщения с уникальным идентификатором блока,
            проверить все ли ожидаемые блоки сообщения пришли - если да - инициирует
            склеивание файлов в один и последующую отправку пользователю,
            затем проверяет нет ли в очереди сообщений, которые приняты полностью,
            если да, то выполняет описанные выше процедуры и для них
        """

        asyncmanager = self.getuserinfo(chatid).getAsyncMgr()
        # Регистрируем факт приема блока по уникальному идентификатору
        asyncid = asyncmanager.onReceiveUniqueId(uniqueid)

        # Пока есть сообщения, которые собрались полностью (и уже ничего не ждут)
        while asyncid != WAIT_MORE:
            number = asyncmanager.numberOnChunks(asyncid)
            # Сливаем все блоки в один
            self.__sendermgr.chunksMerge(chatid, asyncid, number)
            # Посылаем пользователю склееный файл
            await self.__sendermgr.audioSend(chatid, asyncid)
            # Очищаем память, которую занимали сообщения
            #   (Это можно сделать еще на этапе асинхронного получения аудио)
            self.getuserinfo(chatid).getBufferMgr().delMsg(asyncid)
            # Получем идентификтор асинхронной обработки или WAIT_MORE - если сообщение
            #   следующее в очереди не приняло еще все блоки
            asyncid = asyncmanager.isTopReady()


# Настраиваем логирование
logging.basicConfig(level=logging.INFO)

# Создаем главный объект программы
tg_t2s_bot = TGText2SpeechBot(env_config)


# Вешаем обработчики на события
@tg_t2s_bot.dp.message_handler(commands=["start", "help"])
async def welcome(message: types.Message):
    await tg_t2s_bot.show_welcome(message)


@tg_t2s_bot.dp.message_handler()
async def echo(message: types.Message):
    await tg_t2s_bot.do_echo(message)


# Запускаем бота
if __name__ == "__main__":
    executor.start_polling(tg_t2s_bot.dp, skip_updates=True)
