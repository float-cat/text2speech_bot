import logging
import os

from aiogram import Bot
from aiogram import Dispatcher
from aiogram import executor
from aiogram import types
from asyncmgr import WAIT_MORE
from audiosender import SenderMgr
from botcfg import BotCfg
from keyboard import BotKeyboard
from speakers import checklanguage
from speechkit import SpeechKitAdapter

MAX_LEN_SEGMENT = 120

# Enviropment variables
env_config = {}
env_config["API_TOKEN"] = os.environ.get("GLOBAL_TG_TOKEN")
env_config["API_KEY"] = os.environ.get("GLOBAL_API_KEY")
env_config["ID_FOLDER"] = os.environ.get("GLOBAL_ID_FOLDER")


class TGText2SpeechBot(object):
    def __init__(self, env_config):
        # Initialize bot and dispatcher
        self.bot = Bot(token=env_config["API_TOKEN"])
        self.dp = Dispatcher(self.bot)
        self.__keyboard = BotKeyboard()
        # Bot Config
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
        lastidx = len(message.text) - 1
        sexsetup = message.text[1:lastidx]
        if sexsetup == "Женский":
            userinfo.setSex("female")
        else:
            userinfo.setSex("male")
        await self.bot.send_message(
            message.chat.id,
            "Пол голоса был изменен на " + sexsetup.lower(),
            reply_markup=self.__keyboard.getKeyboardsByState("menu"),
        )

    async def change_speed(self, message, userinfo):
        speedsetup = float(message.text[1:])
        userinfo.setSpeed(speedsetup)
        await self.bot.send_message(
            message.chat.id, f"Скорость теперь {speedsetup}", reply_markup=self.__keyboard.getKeyboardsByState("menu")
        )

    async def do_echo(self, message):
        userinfo = self.getuserinfo(message.chat.id)
        elif message.text == "Пoл М/Ж":
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
        userinfo.setLang(checklanguage(message.text))
        asyncid = userinfo.getAsyncMgr().getAsyncId()
        uniqueids = userinfo.getAsyncMgr().genUniqueIdsFree(message.text, MAX_LEN_SEGMENT)
        userinfo.getAsyncMgr().registerChunksNumber(asyncid, len(uniqueids))
        startsegment = 0
        # DBG Добавить пробелы к тексту сообщения, если уник больше длины текста
        await self.bot.send_message(message.chat.id, "Происходит магия...")
        for i in range(0, len(uniqueids)):
            offset = startsegment
            if startsegment > 0:
                offset += 1
            asyncinfo = {"asyncid": asyncid, "uniqueid": uniqueids[i], "offset": offset}
            userinfo.getAsyncMgr().registerUniqueId(asyncid, uniqueids[i])
            await self.__text2speechAdapter.getAudio(message, asyncinfo, i)
            startsegment += uniqueids[i]

    async def onReceivedFile(self, chatid, asyncid, uniqueid):
        asyncmanager = self.getuserinfo(chatid).getAsyncMgr()
        asyncid = asyncmanager.onReceiveUniqueId(uniqueid)
        if asyncid != WAIT_MORE:
            number = asyncmanager.numberOnChunks(asyncid)
            self.__sendermgr.chunksMerge(chatid, asyncid, number)
            await self.__sendermgr.audioSend(chatid, asyncid)
            asyncid = asyncmanager.isTopReady()
            while asyncid != WAIT_MORE:
                number = asyncmanager.numberOnChunks(asyncid)
                self.__sendermgr.chunksMerge(chatid, asyncid, number)
                await self.__sendermgr.audioSend(chatid, asyncid)
                asyncid = asyncmanager.isTopReady()


# Configure logging
logging.basicConfig(level=logging.INFO)

# Create bot
tg_t2s_bot = TGText2SpeechBot(env_config)


# Handlers
@tg_t2s_bot.dp.message_handler(commands=["start"])
async def welcome(message: types.Message):
    await tg_t2s_bot.show_welcome(message)


@tg_t2s_bot.dp.message_handler()
async def echo(message: types.Message):
    await tg_t2s_bot.do_echo(message)


if __name__ == "__main__":
    executor.start_polling(tg_t2s_bot.dp, skip_updates=True)
