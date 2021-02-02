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
env_config["IAM_TOKEN"] = os.environ.get("GLOBAL_IAM_TOKEN")
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
            message.chat.id, "Привет, " + message.from_user.first_name + "!\nЧтобы открыть меню - введи /menu"
        )

    async def show_menu(self, message):
        await self.bot.send_message(
            message.chat.id, "Сменить пол /sex\nСменить спикера /speaker\n" + "Установить скорость в процентах /speed"
        )

    async def show_change_sex(self, message):
        userinfo = self.getuserinfo(message.chat.id)
        if userinfo.getSex() == "male":
            userinfo.setSex("female")
            # Need uses dictionary for male voices
            userinfo.setVoice("Элис", userinfo.getSex())
            await self.bot.send_message(message.chat.id, "Пол голоса был изменен на женский")
        else:
            userinfo.setSex("male")
            # Need uses dictionary for male voices
            userinfo.setVoice("Захар", userinfo.getSex())
            await self.bot.send_message(message.chat.id, "Пол голоса был изменен на мужской")

    async def show_change_speaker(self, message):
        userinfo = self.getuserinfo(message.chat.id)
        userinfo.setDialog("wait_speaker")
        await self.bot.send_message(message.chat.id, speakersinfo.getSpeakersBySex(userinfo.getSex()))

    async def show_change_speed(self, message):
        userinfo = self.getuserinfo(message.chat.id)
        userinfo.setDialog("wait_speed")
        await self.bot.send_message(message.chat.id, "Введите скорость в процентах от 10 до 300")

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
            speed_persents = float(message.text)
            if speed_persents >= 10 and speed_persents <= 300:
                userinfo.setSpeed(speed_persents / 100)
            else:
                userinfo.setDialog("normal")
                await self.bot.send_message(message.chat.id, "Скорость должна быть от 10 до 300 процентов.\n")
                return
            await self.bot.send_message(message.chat.id, f"Скорость x{speed_persents/100}\n")
            userinfo.setDialog("normal")
            return
        userinfo.setLang(checklanguage(message.text))
        with open("audio.ogg", "wb") as f:
            for audio_content in synthesize(env_config["ID_FOLDER"], env_config["IAM_TOKEN"], message.text, userinfo):
                f.write(audio_content)
        f = open("audio.ogg", "rb")
        await self.bot.send_voice(message.from_user.id, f)


# Configure logging
logging.basicConfig(level=logging.INFO)

# Create bot
tg_t2s_bot = TGText2SpeechBot(env_config)


# Handlers
@tg_t2s_bot.dp.message_handler(commands=["start", "help"])
async def welcome(message: types.Message):
    await tg_t2s_bot.show_welcome(message)


@tg_t2s_bot.dp.message_handler(commands=["menu"])
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
