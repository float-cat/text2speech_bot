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
bot_config["speed"] = 1
bot_config["dialog"] = 0

# Speackers names
speakers = {}
speakers['female'] = {
    'Элис': 'alyss', 'Джейн': 'jane',
    'Оксана': 'oksana', 'Омаж': 'omazh'
}
speakers['male'] = {'Захар': 'zahar', 'Ермил': 'ermil'}

# Dialog processing status
gd_status = {
    "normal": 0,
    "wait_speaker": 1,
    "wait_speed": 2
}

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
        "Сменить пол /sex\nСменить спикера /speaker\n" +
        "Установить скорость в процентах /speed"
    )


@dp.message_handler(commands=["sex"])
async def change_sex(message: types.Message):
    if bot_config["sex"] == "male":
        bot_config["sex"] = "female"
        # Need uses dictionary for male voices
        bot_config["voice"] = 'alyss'
        await bot.send_message(
            message.chat.id,
            "Пол голоса был изменен на женский"
        )
    else:
        bot_config["sex"] = "male"
        # Need uses dictionary for male voices
        bot_config["voice"] = 'zahar'
        await bot.send_message(
            message.chat.id,
            "Пол голоса был изменен на мужской"
        )


@dp.message_handler(commands=["speaker"])
async def change_speaker(message: types.Message):
    speaker_list = ""
    for speaker in speakers[bot_config["sex"]].keys():
        speaker_list += speaker + " "
    bot_config["dialog"] = gd_status["wait_speaker"]
    await bot.send_message(message.chat.id, speaker_list)
    
@dp.message_handler(commands=["speed"])
async def change_speed(message: types.Message):
    bot_config["dialog"] = gd_status["wait_speed"]
    await bot.send_message(
        message.chat.id,
        'Введите скорость в процентах от 10 до 300'
    )


@dp.message_handler()
async def echo(message: types.Message):
    if len(message.text) > 4000:
        await bot.send_message(
            message.chat.id,
            "Слишком большое сообщение, надо не больше 4000 символов"
        )
        return
    if bot_config["dialog"] == gd_status["wait_speaker"]:
        if message.text in speakers[bot_config["sex"]].keys():
            bot_config["voice"] = speakers[bot_config["sex"]][message.text]
            await bot.send_message(
                message.chat.id, "Спикер изменен на " + message.text
            )
            bot_config["dialog"] = gd_status["normal"]
            return
    elif bot_config["dialog"] == gd_status["wait_speed"]:
        speed_persents = float(message.text)
        if speed_persents >= 10 and speed_persents <= 300:
            bot_config["speed"] = speed_persents / 100
        else:
            await bot.send_message(
                message.chat.id, "Скорость должна быть от 10 до 300 процентов.\n"
            )
            return
        await bot.send_message(
            message.chat.id, f"Скорость x{speed_persents/100}\n"
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
    f = open("audio.ogg", "rb")
    await bot.send_voice(message.from_user.id, f)
    synthesize(
        env_config["ID_FOLDER"],
        env_config["IAM_TOKEN"],
        message.text, bot_config
    )


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
