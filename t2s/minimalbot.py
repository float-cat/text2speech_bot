# minimalbot для проверки функций получения и отправки аудио
import os

import sk_adapter
import telebot

bot_config = {}
bot_config["TG_SEX"] = "male"
bot_config["TG_TOKEN"] = os.environ.get("TG_TOKEN")
bot_config["GLOBAL_IAM_TOKEN"] = os.environ.get("IAM_TOKEN")
bot_config["GLOBAL_ID_FOLDER"] = os.environ.get("ID_FOLDER")

bot = telebot.TeleBot(bot_config["TG_TOKEN"])


@bot.message_handler(commands=["start"])
def start_message(message):
    bot.send_message(
        message.chat.id, "Привет, " + message.from_user.first_name + "!\nИспользуй команду /changesex для смены пола"
    )


@bot.message_handler(commands=["changesex"])
def sexchange_message(message):
    if bot_config["TG_SEX"] == "male":
        bot_config["TG_SEX"] = "female"
        bot.send_message(message.chat.id, "Пол голоса был изменен на женский")
    else:
        bot_config["TG_SEX"] = "male"
        bot.send_message(message.chat.id, "Пол голоса был изменен на мужской")


@bot.message_handler(content_types=["text"])
def send_text(message):
    # sk_adapter.getAudio(message.from_user.username,
    # bot_config['GLOBAL_IAM_TOKEN'],
    # bot_config['GLOBAL_ID_FOLDER'], message.text)
    sk_adapter.getAudio(
        message.from_user.username, sk_adapter.rus_to_translite(message.text.lower()), bot_config["TG_SEX"]
    )
    sk_adapter.botSendAudio(bot, message.from_user.username, message.chat.id)


bot.polling()
