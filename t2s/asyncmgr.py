# System for management audio segments
import time


MERGE_TIMEOUT = 2
END_OF_CHUNKS = 100
WAIT_CHUNK_DATA = 0
DATA_RECEIVED = 1
WAIT_ALL_INFO = 0
WAIT_ALL_DATA = 1
RECEIVED_ALL_DATA = 2
WAIT_MORE = 300


class ChunkInfo(object):
    def __init__(self, uniqueid):
        self.__uniqueid = uniqueid
        self.__status = WAIT_CHUNK_DATA

    def getUniqueId(self):
        return self.__uniqueid

    def setDataReceived(self):
        self.__status = DATA_RECEIVED

    def getDataReceived(self):
        return self.__status == DATA_RECEIVED

    def isDataReceived(self):
        return self.__uniqueid == DATA_RECEIVED


class AsyncInfo(object):
    def __init__(self):
        self.__status = WAIT_ALL_INFO
        self.__chunks = []

    def setUniqueID(self, uniqueid):
        self.__chunks.append(ChunkInfo(uniqueid))

    def setStatusWaitAllData(self):
        self.__status = WAIT_ALL_DATA

    def isMyUnique(self, uniqueid):
        retval = False
        number = 0
        for chunk in self.__chunks:
            if chunk.getUniqueId() == uniqueid:
                chunk.setDataReceived()
                retval = False
            if chunk.getDataReceived():
                number += 1
        if number == len(self.__chunks):
            self.__status = RECEIVED_ALL_DATA
        return retval

    def isReceivedAllData(self):
        return self.__status == RECEIVED_ALL_DATA

    def getChunksInfo(self):
        return self.__chunks


class AsyncMgr(object):
    def __init__(self):
        self.__firstid = 0
        self.__asyncid = -1
        self.__lasttime = 0
        self.__asynctasks = []

    def updateAsync(self):
        newtime = time.time()
        if newtime - self.__lasttime > MERGE_TIMEOUT:
            if self.__asyncid > -1:
                self.__asynctasks[self.__asyncid].setStatusWaitAllData()
            return True
        return False
        self.__lasttime = newtime

    def getAsyncId(self):
        if self.updateAsync():
            self.__asyncid = self.__asyncid + 1
            self.__asynctasks.append(AsyncInfo())
        return self.__asyncid

    def registerUniqueId(self, asyncid, uniqueid):
        self.updateAsync()
        self.__asynctasks[asyncid].setUniqueID(uniqueid)

    def onReceiveUniqueId(self, uniqueid):
        self.updateAsync()
        for i in range(self.__firstid, self.__asyncid + 1):
            if self.__asynctasks[i].isMyUnique(uniqueid):
                break
        return self.isTopReady()

    def isTopReady(self):
        retval = WAIT_MORE
        if self.__asyncid < self.__firstid:
            return retval
        if self.__asynctasks[self.__firstid].isReceivedAllData():
            retval = self.__firstid
            self.__firstid += 1
        return retval
