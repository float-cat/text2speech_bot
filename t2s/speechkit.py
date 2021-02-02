import requests


def checklanguage(text):
    rus = 0
    eng = 0
    for char in text.lower():
        if char >= "а" and char <= "я":
            rus += 1
        elif char >= "a" and char <= "z":
            eng += 1
    if eng < rus:
        return "ru-RU"
    return "en-US"


def synthesize(folder_id, api_key, text, userinfo):
    url = "https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize"
    headers = {"Authorization": "Api-Key " + api_key}
    voiceid = userinfo.getVoice()
    if voiceid == 'filipp':
        voiceid = 'zahar'
    elif voiceid == 'alena':
        voiceid = 'alyss'
    data = {
        "text": text,
        "lang": userinfo.getLang(),
        "folderId": folder_id,
        "speed": userinfo.getSpeed(),
        "voice": voiceid
    }

    with requests.post(url, headers=headers, data=data, stream=True) as resp:
        if resp.status_code != 200:
            raise RuntimeError("Invalid response received: code: %d, message: %s" % (resp.status_code, resp.text))

        for chunk in resp.iter_content(chunk_size=None):
            yield chunk
