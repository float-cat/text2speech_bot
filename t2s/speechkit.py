import requests

from t2s.speakers import Speakers


speakersinfo = Speakers()


def synthesize(folder_id, api_key, text, userinfo):

    url = "https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize"
    headers = {"Authorization": "Api-Key " + api_key}

    data = {
        "text": text,
        "lang": userinfo.getLang(),
        "folderId": folder_id,
        "speed": userinfo.getSpeed(),
        "voice": speakersinfo.getSpeakerId(userinfo.getLang(), userinfo.getSex()),
    }

    with requests.post(url, headers=headers, data=data, stream=True) as resp:

        if resp.status_code != 200:
            raise RuntimeError("Invalid response received: code: %d, message: %s" % (resp.status_code, resp.text))

        for chunk in resp.iter_content(chunk_size=None):
            yield chunk
