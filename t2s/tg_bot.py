import logging
from speechkit import synthesize
from aiogram import Bot, Dispatcher, executor, types
from config import API_TOKEN, FOLDER_ID, IAM_TOKEN

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.answer("Comptech 2021\nText To Speech Bot.")

@dp.message_handler()
async def echo(message: types.Message):
    with open('audio.ogg', "wb") as f:
        for audio_content in synthesize(FOLDER_ID, IAM_TOKEN, message.text):
            f.write(audio_content)
    f = open('audio.ogg', 'rb')
    await bot.send_voice(message.from_user.id, f)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)