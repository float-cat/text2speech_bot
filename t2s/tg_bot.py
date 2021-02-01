import logging
import os

from aiogram import Bot
from aiogram import Dispatcher
from aiogram import executor
from aiogram import types
from speechkit import checklanguage
from speechkit import synthesize

# Enviropment variables
env_config = {}
env_config["API_TOKEN"] = os.environ.get("GLOBAL_TG_TOKEN")
env_config["IAM_TOKEN"] = os.environ.get("GLOBAL_IAM_TOKEN")
env_config["ID_FOLDER"] = os.environ.get("GLOBAL_ID_FOLDER")

# Bot Config
bot_config = {}
bot_config["sex"] = 'male'
bot_config["voice"] = 'zahar'
bot_config["dialog"] = 0

# Speackers names
speakers = {}
speakers['female'] = {
    'alyss': 'Элис', 'jane': 'Джейн',
    'oksana': 'Оксана', 'omazh': 'Омаж'
}
speakers['male'] = {'zahar': 'Захар', 'ermil': 'Ермил'}

# Dialog processing status
gd_status = {"normal": 0, "wait_speaker": 1}

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=env_config["API_TOKEN"])
dp = Dispatcher(bot)


@dp.message_handler(commands=["start", "help"])
async def send_welcome(message: types.Message):
    await bot.send_message(
        message.chat.id, "Привет, " + message.from_user.first_name +
        "!\nЧтобы открыть меню - введи /menu"
    )


@dp.message_handler(commands=["menu"])
async def send_menu(message: types.Message):
    await bot.send_message(
        message.chat.id,
        "Сменить пол /sex\nСменить спикера /speaker"
    )


@dp.message_handler(commands=["sex"])
async def change_sex(message: types.Message):
    if bot_config["sex"] == "male":
        bot_config["sex"] = "female"
        # Need uses dictionary for male voices
        bot_config["voice"] = speakers["female"].keys()[0]
        await bot.send_message(
            message.chat.id,
            "Пол голоса был изменен на женский"
        )
    else:
        bot_config["sex"] = "male"
        # Need uses dictionary for male voices
        bot_config["voice"] = speakers["male"].keys()[0]
        await bot.send_message(
            message.chat.id,
            "Пол голоса был изменен на мужской"
        )


@dp.message_handler(commands=["speaker"])
async def change_speaker(message: types.Message):
    speaker_list = ""
    for speaker in speakers[bot_config["sex"]].keys():
        speaker_list += speakers[bot_config["sex"]][speaker] + " "
    bot_config["dialog"] = gd_status["wait_speaker"]
    await bot.send_message(message.chat.id, speaker_list)


@dp.message_handler()
async def echo(message: types.Message):
    if bot_config["dialog"] == gd_status["wait_speaker"]:
        if message.text in speakers[bot_config["sex"]].keys():
            bot_config["voice"] = message.text
            await bot.send_message(
                message.chat.id, "Спикер изменен на " +
                speakers[bot_config["sex"]][message.text]
            )
            bot_config["dialog"] = gd_status["normal"]
            return
    else:
        bot_config["dialog"] = gd_status["normal"]
    bot_config["lang"] = checklanguage(message.text)
    with open("audio.ogg", "wb") as f:
        for audio_content in synthesize(
            env_config["ID_FOLDER"],
            env_config["IAM_TOKEN"],
            message.text, bot_config
        ):
            f.write(audio_content)
            f.close()
    f = open("audio.ogg", "rb")
    await bot.send_voice(message.from_user.id, f)
    synthesize(
        env_config["ID_FOLDER"],
        env_config["IAM_TOKEN"],
        message.text, bot_config
    )


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
