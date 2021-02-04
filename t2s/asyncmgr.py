# System for management audio segments
import time


MERGE_TIMEOUT = 2
END_OF_CHUNKS = 100
WAIT_CHUNK_DATA = 0
DATA_RECEIVED = 1
WAIT_ALL_INFO = 0
WAIT_ALL_DATA = 1
RECEIVED_ALL_DATA = 2

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
        self.__chunkid = 0
        self.__status = WAIT_ALL_INFO
        self.__chunks = []

    def setUniqueID(self, chunkid, uniqueid):
        self.__chunks[chunkid] = ChunkInfo(uniqueid)
        self.__chunkid += 1

    def setStatusWaitAllData(self):
        self.__status = WAIT_ALL_DATA

    def isMyUnique(self, uniqueid):
        retval = False
        number = 0
        for chunk in self.__chunks:
            if chunk.getUniqueId() == uniquid:
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
        self.__lastTime = time.time()
        self.__asynctasks = []

    def getAsyncId(self):
        newtime = time.time()
        if newtime - self.__lastlime > MERGE_TIMEOUT:
            if self.__asyncid > -1:
                self.__asynctasks[self.__asyncid].setStatusWaitAllData()
            self.__asyncid == (self.__asyncid + 1)
            self.__asynctasks[self.__asyncid] = AsyncInfo()
        self.__lastlime = newtime
        return self.__asyncid

    def onReceiveUniqueID(self, uniqueid):
        retval = WAIT_MORE
        for i in range(self.__firstid, self.__asyncid - 1):
            if task.isMyUnique(uniqueid):
                break;
            i += 1
        if self.__asynctasks[self.__firstid].isReceivedAllData():
            retval self.__firstid
        return retval
