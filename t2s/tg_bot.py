import logging
import os

from aiogram import Bot
from aiogram import Dispatcher
from aiogram import executor
from aiogram import types
from botcfg import BotCfg
from botcfg import speakersinfo
from speechkit import checklanguage
from speechkit import synthesize

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
        # Bot Config
        self.__botcfg = BotCfg()

    def getuserinfo(self, chatid):
        return self.__botcfg.userInfo(chatid)

    async def show_welcome(self, message):
        await self.bot.send_message(
            message.chat.id, "Привет, " + message.from_user.first_name + "!\nЧтобы открыть меню - введи /help"
        )

    async def show_menu(self, message):
        await self.bot.send_message(
            message.chat.id, "Сменить пол /sex\nСменить спикера /speaker\n" + "Установить скорость /speed"
        )

    async def show_change_sex(self, message):
        userinfo = self.getuserinfo(message.chat.id)
        if userinfo.getSex() == "male":
            userinfo.setSex("female")
            # Need uses dictionary for male voices
            userinfo.setVoice("Алена", userinfo.getSex())
            await self.bot.send_message(message.chat.id, "Пол голоса был изменен на женский, спикер - Алена")
        else:
            userinfo.setSex("male")
            # Need uses dictionary for male voices
            userinfo.setVoice("Филипп", userinfo.getSex())
            await self.bot.send_message(message.chat.id, "Пол голоса был изменен на мужской, спикер Филипп")

    async def show_change_speaker(self, message):
        userinfo = self.getuserinfo(message.chat.id)
        userinfo.setDialog("wait_speaker")
        await self.bot.send_message(message.chat.id, speakersinfo.getSpeakersBySex(userinfo.getSex()))

    async def show_change_speed(self, message):
        userinfo = self.getuserinfo(message.chat.id)
        userinfo.setDialog("wait_speed")
        await self.bot.send_message(message.chat.id, "Выберите скорость из списка доступных:\n0.5, 1, 1.5, 2.\n")

    async def do_echo(self, message):
        userinfo = self.getuserinfo(message.chat.id)
        if len(message.text) > 4000:
            await self.bot.send_message(message.chat.id, "Слишком большое сообщение, надо не более 4000 символов")
            return
        if userinfo.checkDialog("wait_speaker"):
            if speakersinfo.isSpeaker(message.text, userinfo.getSex()):
                userinfo.setVoice(message.text, userinfo.getSex())
                await self.bot.send_message(message.chat.id, "Спикер изменен на " + message.text)
                userinfo.setDialog("normal")
                return
            else:
                userinfo.setDialog("normal")
        elif userinfo.checkDialog("wait_speed"):
            if userinfo.isCorrectSpeed(message.text):
                userinfo.setSpeed(message.text)
            else:
                userinfo.setDialog("normal")
                await self.bot.send_message(message.chat.id, "Скорость должна быть из списка:\n0.5, 1, 1.5, 2.\n")
                return
            await self.bot.send_message(message.chat.id, "Скорость x" + message.text + "\n")
            userinfo.setDialog("normal")
            return
        userinfo.setLang(checklanguage(message.text))
        with open("audio.ogg", "wb") as f:
            await self.bot.send_message(message.chat.id, "Происходит магия...")
            try:
                for audio_content in synthesize(
                    env_config["ID_FOLDER"], env_config["API_KEY"], message.text, userinfo
                ):
                    f.write(audio_content)
            except RuntimeError:
                print("test")
                await self.bot.send_message(message.chat.id, "Похоже что волшебная\nпалочка сломалась :(")
        f = open("audio.ogg", "rb")
        await self.bot.send_voice(message.from_user.id, f)


# Configure logging
logging.basicConfig(level=logging.INFO)

# Create bot
tg_t2s_bot = TGText2SpeechBot(env_config)


# Handlers
@tg_t2s_bot.dp.message_handler(commands=["start"])
async def welcome(message: types.Message):
    await tg_t2s_bot.show_welcome(message)


@tg_t2s_bot.dp.message_handler(commands=["help"])
async def menu(message: types.Message):
    await tg_t2s_bot.show_menu(message)


@tg_t2s_bot.dp.message_handler(commands=["sex"])
async def change_sex(message: types.Message):
    await tg_t2s_bot.show_change_sex(message)


@tg_t2s_bot.dp.message_handler(commands=["speaker"])
async def change_speaker(message: types.Message):
    await tg_t2s_bot.show_change_speaker(message)


@tg_t2s_bot.dp.message_handler(commands=["speed"])
async def change_speed(message: types.Message):
    await tg_t2s_bot.show_change_speed(message)


@tg_t2s_bot.dp.message_handler()
async def echo(message: types.Message):
    await tg_t2s_bot.do_echo(message)


if __name__ == "__main__":
    executor.start_polling(tg_t2s_bot.dp, skip_updates=True)
