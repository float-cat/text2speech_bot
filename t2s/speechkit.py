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

    async def getAudio(self, chatid, text, asyncinfo, fileid):
        asyncid = asyncinfo["asyncid"]
        uniqueid = asyncinfo["uniqueid"]
        offset = asyncinfo["offset"]
        userinfo = self.__t2sbot.getuserinfo(chatid)
        audiofile = "synthesizes/%d_%d_%d.ogg" % (chatid, asyncid, fileid)
        with open(audiofile, "wb") as f:
            try:
                shift = offset + uniqueid
                for audio_content in self.synthesize(text[offset:shift], userinfo):
                    f.write(audio_content)
                f.close()
                userinfo.getAsyncMgr().registerUniqueId(asyncid, uniqueid)
                await self.__t2sbot.onReceivedFile(chatid, asyncid, uniqueid)

            except RuntimeError:
                self.__t2sbot.bot.send_message(chatid, "Похоже что волшебная палочка сломалась :(")
