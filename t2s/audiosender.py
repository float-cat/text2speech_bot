# Merge files and send
import os
from pydub import AudioSegment


class SenderMgr(object):
    def __init__(self, t2sbot):
        self.__t2sbot = t2sbot

    def chunksMerge(self, chatid, asyncid, number):
        audiooutputfile = "synthesizes/%d_%d.ogg" % (chatid, asyncid)
        if number == 1:
            os.rename(
                "synthesizes/%d_%d_0.ogg" % (chatid, asyncid),
                "synthesizes/%d_%d.ogg" % (chatid, asyncid)
            )
            return
        audiofile1 = "synthesizes/%d_%d_0.ogg" % (chatid, asyncid)
        audiofile2 = "synthesizes/%d_%d_1.ogg" % (chatid, asyncid)
        filecontent1 = AudioSegment.from_ogg(audiofile1)
        filecontent2 = AudioSegment.from_ogg(audiofile2)
        os.remove(audiofile1)
        os.remove(audiofile2)
        outputfile = filecontent1 + filecontent2
        for i in range(2, number):
            audiofile = "synthesizes/%d_%d_%d.ogg" % (chatid, asyncid, i)
            inputfile = AudioSegment.from_ogg(audiofile)
            outputfile += inputfile
            os.remove(audiofile)
        outputfile.export(audiooutputfile, format="ogg")

    async def audioSend(self, chatid, asyncid):
        audiofile = "synthesizes/%d_%d.ogg" % (chatid, asyncid)
        f = open(audiofile, "rb")
        await self.__t2sbot.bot.send_voice(chatid, f)
        f.close()
        os.remove(audiofile)
