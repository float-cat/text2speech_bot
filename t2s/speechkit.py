import requests
from speakers import Speakers


speakersinfo = Speakers()


class SpeechKitAdapter(object):
    def __init__(self, folder_id, api_key, t2sbot):
        self.__folder_id = folder_id
        self.__api_key = api_key
        self.__t2sbot = t2sbot

    def synthesize(self, text, userinfo):
        url = "https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize"
        headers = {"Authorization": "Api-Key " + self.__api_key}
        data = {
            "text": text,
            "lang": userinfo.getLang(),
            "folderId": self.__folder_id,
            "speed": userinfo.getSpeed(),
            "voice": speakersinfo.getSpeakerId(userinfo.getLang(), userinfo.getSex()),
        }

        with requests.post(url, headers=headers, data=data, stream=True) as resp:
            if resp.status_code != 200:
                raise RuntimeError("Invalid response received: code: %d, message: %s" % (resp.status_code, resp.text))

            for chunk in resp.iter_content(chunk_size=None):
                yield chunk

    async def getAudio(self, message, asyncinfo, fileid):
        asyncid = asyncinfo["asyncid"]
        uniqueid = asyncinfo["uniqueid"]
        offset = asyncinfo["offset"]
        userinfo = self.__t2sbot.getuserinfo(message.chat.id)
        audiofile = "synthesizes/%d_%d_%d.ogg" % (message.chat.id, asyncid, fileid)
        with open(audiofile, "wb") as f:
            try:
                shift = offset + uniqueid
                for audio_content in self.synthesize(message.text[offset:shift], userinfo):
                    f.write(audio_content)
                f.close()
                await self.__t2sbot.onReceivedFile(message.chat.id, asyncid, uniqueid)

            except RuntimeError:
                await self.__t2sbot.bot.send_message(message.chat.id, "Похоже что волшебная палочка сломалась :(")
