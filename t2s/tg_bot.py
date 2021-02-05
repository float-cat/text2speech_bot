import logging
import os

from aiogram import Bot
from aiogram import Dispatcher
from aiogram import executor
from aiogram import types

from t2s.botcfg import BotCfg
from t2s.keyboard import BotKeyboard
from t2s.preprocessing import TextPreprocessing
from t2s.speakers import checklanguage
from t2s.speechkit import synthesize

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

        lastidx = len(message.text) - 1
        speedsetup = float(message.text[1:lastidx])

        userinfo.setSpeed(speedsetup)

        await self.bot.send_message(
            message.chat.id, f"Скорость теперь {speedsetup}", reply_markup=self.__keyboard.getKeyboardsByState("menu")
        )

    async def do_echo(self, message):

        userinfo = self.getuserinfo(message.chat.id)

        if len(message.text) > 4000:
            await self.bot.send_message(message.chat.id, "Слишком большое сообщение, надо не более 4000 символов")

            return

        elif message.text == "[Пол М/Ж]":
            await self.bot.send_message(
                message.chat.id, "Выберите пол", reply_markup=self.__keyboard.getKeyboardsByState("sex")
            )

            return

        elif self.__keyboard.isSexSetup(message.text):
            await self.change_sex(message, userinfo)

            return

        elif message.text == "[Скорость]":

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
        audiofile = message.from_user.username + "_audio.ogg"

        with open(audiofile, "wb") as f:

            await self.bot.send_message(message.chat.id, "Происходит магия...")

            try:

                for audio_content in synthesize(
                    env_config["ID_FOLDER"], env_config["API_KEY"], TextPreprocessing(message.text), userinfo
                ):
                    f.write(audio_content)

            except RuntimeError:
                await self.bot.send_message(message.chat.id, "Похоже что волшебная палочка сломалась :(")

        f = open(audiofile, "rb")
        await self.bot.send_voice(message.from_user.id, f)


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
