# System for management audio segments
import time


MERGE_TIMEOUT = 1
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
        self.__number = 0
        self.__received = 0

    def setUniqueID(self, uniqueid):
        self.__chunks.append(ChunkInfo(uniqueid))

    def setStatusWaitAllData(self):
        self.__status = WAIT_ALL_DATA

    def isMyUnique(self, uniqueid):
        retval = False
        for chunk in self.__chunks:
            if chunk.getUniqueId() == uniqueid:
                chunk.setDataReceived()
                self.__received += 1
                retval = True
                break
        if self.__number == self.__received:
            self.__status = RECEIVED_ALL_DATA
        return retval

    def isUniqueFree(self, uniqueid):
        for chunk in self.__chunks:
            if chunk.getUniqueId() == uniqueid:
                return False
        return True

    def regChunksNumber(self, number):
        self.__number += number

    def getChunksNumber(self):
        return self.__number

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
        self.__uidcandidates = []

    def updateAsync(self):
        newtime = time.time()
        if newtime - self.__lasttime > MERGE_TIMEOUT:
            self.__lasttime = newtime
            if self.__asyncid > -1:
                self.__asynctasks[self.__asyncid].setStatusWaitAllData()
            return True
        return False

    def getAsyncId(self):
        if self.updateAsync():
            self.__asyncid = self.__asyncid + 1
            self.__asynctasks.append(AsyncInfo())
        return self.__asyncid

    def registerUniqueId(self, asyncid, uniqueid):
        self.updateAsync()
        self.__asynctasks[asyncid].setUniqueID(uniqueid)

    def registerChunksNumber(self, asyncid, number):
        self.__asynctasks[self.__asyncid].regChunksNumber(number)

    def onReceiveUniqueId(self, uniqueid):
        self.updateAsync()
        for i in range(self.__firstid, self.__asyncid + 1):
            if self.__asynctasks[i].isMyUnique(uniqueid):
                break
        return self.isTopReady()

    def isUniqueFree(self, uniqueid):
        self.updateAsync()
        for i in range(self.__firstid, self.__asyncid + 1):
            if not self.__asynctasks[i].isUniqueFree(uniqueid):
                return False
        for i in self.__uidcandidates:
            if i == uniqueid:
                return False
        self.__uidcandidates.append(uniqueid)
        return True

    def clearCandidates(self):
        self.__uidcandidates.clear()

    def whereNearSpace(self, text, uniqueid, offset):
        idx = offset + uniqueid
        if len(text) == idx or text[idx] == " ":
            return uniqueid
        i = idx
        while i >= offset and text[i] != " ":
            i -= 1
        if i <= offset:
            return uniqueid
        return i - offset

    def genUniqueIdsFree(self, text, segmentlen):
        retval = []
        length = len(text)
        numberofsegments = length // segmentlen
        offset = 0
        uniqueid = 0
        tail = 0
        tmpval = 0
        while len(retval) < numberofsegments:
            uniqueid = segmentlen + tail
            tmpval = self.whereNearSpace(text, uniqueid, offset)
            tail = uniqueid - tmpval
            uniqueid = tmpval
            checkwhileunless = 0
            while not self.isUniqueFree(uniqueid):
                if offset + uniqueid == length:
                    uniqueid += 1
                    continue
                checkwhileunless += 1
                if checkwhileunless > 20:
                    quit()
                uniqueid -= 1
                tmpval = self.whereNearSpace(text, uniqueid, offset)
                tail += uniqueid - tmpval
                uniqueid = tmpval
            retval.append(uniqueid)
            offset += uniqueid
        if offset < length:
            retval.append(length - offset)
        self.clearCandidates()
        return retval

    def isTopReady(self):
        retval = WAIT_MORE
        if self.__asyncid < self.__firstid:
            return retval
        if self.__asynctasks[self.__firstid].isReceivedAllData():
            retval = self.__firstid
            self.__firstid += 1
        return retval

    def numberOnChunks(self, asyncid):
        return self.__asynctasks[asyncid].getChunksNumber()
