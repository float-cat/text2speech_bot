# Функции получения аудио от яндекс.клауд и отправки пользователю
import os

import requests

# For yandex cloud service
# def getAudio(username, IAM_TOKEN, ID_FOLDER, text, sex):
#     url = 'https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize'
#     voicetype = 'alyss'
#     if sex == 'male':
#         voicetype = 'zahar'
#     headers = {
#         'Authorization': f'Bearer {IAM_TOKEN}',
#         'folderId': ID_FOLDER,
#         'format': 'mp3',
#         'text': text,
#         'lang': 'ru-RU',
#         'speed': 1,
#         'voice': voicetype,
#         'emotion': 'good'
#     }
#     r = requests.post(url, headers)
#     f = open (username + "_result.mp3", 'wb')
#     f.write(r.content)
#     f.close()

trdict = {
    "а": "a",
    "б": "b",
    "в": "v",
    "г": "g",
    "д": "d",
    "е": "e",
    "ё": "ye",
    "ж": "zh",
    "з": "z",
    "и": "i",
    "й": "iy",
    "к": "k",
    "л": "l",
    "м": "m",
    "н": "n",
    "о": "o",
    "п": "p",
    "р": "r",
    "с": "s",
    "т": "t",
    "у": "y",
    "ф": "f",
    "х": "kh",
    "ц": "tsc",
    "ч": "ch",
    "ш": "sh",
    "щ": "sch",
    "ъ": "",
    "ы": "i",
    "ь": "",
    "э": "e",
    "ю": "u",
    "я": "ya",
}


# For transliteration
def rus_to_translite(text):
    result = ""
    for val in text:
        if trdict.get(val):
            result += trdict[val]
        else:
            result += val
    return result


# For free simple text2speech system (english only)
def getAudio(username, text, sex):
    url = "https://www.text2speech.org/"
    voicetype = "Female US"
    if sex == "male":
        voicetype = "Male US"
    headers = {"text": text, "voice": voicetype, "speed": "Normal", "outname": username + "_result"}
    # Передаем запрос на получение ссылки ответа
    r = requests.post(url, headers)
    answerHTML = r.content.decode("utf-8")
    # Вырезаем адрес ответа t2s так, чтобы не захватить кавычки
    idxstart = answerHTML.find("var url = ") + 11
    idxend = answerHTML.find(";", idxstart) - 1
    # Передаем запрос на получение ссылки файла с аудио
    r = requests.post(url + answerHTML[idxstart:idxend])
    answerHTML = r.content.decode("utf-8")
    # Вырезаем адрес аудио файла игнорируя кавычки
    idxstart = answerHTML.find("source src=") + 12
    idxend = answerHTML.find(">", idxstart) - 1
    # Забираем файл
    r = requests.post(url + answerHTML[idxstart:idxend])
    f = open(username + "_result.mp3", "wb")
    f.write(r.content)
    f.close()


def botSendAudio(bot, username, chatid):
    audio = open(username + "_result.mp3", "rb")
    bot.send_audio(chatid, audio, title="Преобразование завершено")
    audio.close()
    os.remove(username + "_result.mp3")
