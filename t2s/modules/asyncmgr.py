import time

# Следующие значения не должны изменяться в процессе работы программы!
MERGE_TIMEOUT = 1
END_OF_CHUNKS = 100
WAIT_CHUNK_DATA = 0
DATA_RECEIVED = 1
WAIT_ALL_INFO = 0
WAIT_ALL_DATA = 1
RECEIVED_ALL_DATA = 2
WAIT_MORE = 300


class ChunkInfo(object):
    """Класс ChunkInfo хранит информацию о блоке (неважно чего)

    Основное применение - обеспечение удобной проверки статус принятия
    сообщения с уникальным идентификатором

    Атрибуты
    --------
    unqiueid
        уникальный идентификатор блока

    Методы
    ------
    getUniqueId
        позволяет получить уникальный идентификатор блока
    setDataReceived
        метод для установки статуса сообщение принято
    isDataReceived
        метод проверяет приняты ли данные для блока
    """

    def __init__(self, uniqueid):
        self.__uniqueid = uniqueid
        self.__status = WAIT_CHUNK_DATA

    def getUniqueId(self):
        return self.__uniqueid

    def setDataReceived(self):
        self.__status = DATA_RECEIVED

    def isDataReceived(self):
        return self.__status == DATA_RECEIVED


class AsyncInfo(object):
    """Класс AsyncInfo хранит информацию о группе блоков

    Основное применение - учет блоков для проверки статуса приема
    данных. Данный класс является логически связанным с идентификатором
    асинхронной обработки

    Атрибуты
    --------
    пусто

    Методы
    ------
    setUniqueID
        устанавливает (регистрирует/добавляет) уникальный идентификатор блока
        в группе блоков
    setStatusWaitAllData
        переключается в статус ждем сообщения
    isMyUnique
        проверяет занят ли кем-то уникальный идентификатор, и если занят
        то регистрирует факт принятия блока с уникальным идентификатором
    isUniqueFree
        проверяет занят ли кем-то уникальный идентификатор, но ничего не
        меняет
    regChunksNumber
        регистрирует дополнительное ожидаемое число блоков
    getChunksNumber
        возвращает число зарегистрированных блоков
    isReceivedAllData
        проверяет прияны ли данные всех блоков
    getChunksInfo
        дает доступ к приватному полю со списком блоков

    Примечание
    ----------
    Метод getChunksInfo небезопасен, так как возвращает приватное поле,
    доступное для изменения (а в нем хранится важный список, который должен
    быть строго инкапсулирован)
    """

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
        """Метод регистрации факта приема данных по уникальному идентификатору
        Вход: уникальный идентификатор блока
        Выход: ИСТИНА - если в группе блоков есть блок соответствующий уникальному
            идентификатору, иначе ЛОЖЬ
        Задача: зарегистрировать факт приема данных
        """

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
    """Класс AsyncMgr реализует ступенчатый нумератор,
    обработку уникальных идентификаторов и интерфейс отложенной очереди

    Основное применение - организация однозначного индексирования для
    асинхронной работы, подчиняется логике ступенчатого нумератора,
    предовтавляет методы для обработки отложенной очереди из группы блоков

    Атрибуты
    --------
    пусто

    Методы
    ------
    updateAsync
        оновляет статус таймоута (так как таймаут в данном
        классе реалезован не через таймер - то данная фунцкия
        должна вызваться в узких местах, ожидающих проверку
        таймаута)
    getAsyncId
        выдает дейстительный идентификатор асинхронной обработки
    registerUniqueId
        регистрирует уникальный идентификатор на ожидаение приема данных
    registerChunksNumber
        регистрирует дополнительное число блоков
    onReceiveUniqueId
        регистрирует факт принятия данных для уникального идентификатора
    isUniqueFree
        проверяет уникальность идентификатора относительно уже находящихся
        в структуре класса, если идентификатор уникален - помещает его в
        список кандидатов, чтобы учитывать при следующей проверке тоже
    clearCandidates
        очищет список кандидатов уникальных идентификаторов
    whereNearSpace
        ищет ближайший пробел в тексте двигаясь к началу
    genUniqueIdsFree
        передает список уникальных идентификаторов для сообщения,
        в контексте общей задачи это используется для разбивки текста на блоки
    isTopReady
        проверяет первого в очереди на готовность компоновать данные
        (если все блоки приняли данные)
    numberOnChunks
        возвращает количество блоков
    """

    def __init__(self):
        self.__firstid = 0
        self.__asyncid = -1
        self.__lasttime = 0
        self.__asynctasks = []
        self.__uidcandidates = []

    def updateAsync(self):
        """Метод обновляет статус таймаута
        Вход: пусто
        Выход: ИСТИНА - если время истекло, иначе - ЛОЖЬ
        Задача: проверить истекло время или нет и приготовиться
        ждать данные для следующего идентификатора асинхронной обработки
        """

        newtime = time.time()
        # Проверяем разницу между текущим временем и сохраненным
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
        """Метод проверки уникальности идентификатора
        Вход: уникальный идентификатор блока
        Выход: ИСТИНА - если уникален относительно остальных, иначе ЛОЖЬ
        Задача: проверить уникальность идентификатора при подборе
        """

        self.updateAsync()
        # Сравниваем с уникальными идентификаторами в группах блоков
        for i in range(self.__firstid, self.__asyncid + 1):
            if not self.__asynctasks[i].isUniqueFree(uniqueid):
                return False
        # Сравниваем с кандидатами
        for i in self.__uidcandidates:
            if i == uniqueid:
                return False
        # Идентификатор уникален, добавляем его в список кандидатов
        self.__uidcandidates.append(uniqueid)
        return True

    def clearCandidates(self):
        self.__uidcandidates.clear()

    def whereNearSpace(self, text, uniqueid, offset):
        """Метод ищет ближайший слев пробел для исключения ситуации рассечения слов
        Вход: текст, уникальный идентификатор, смещение относительно начала текста
        Выход: позицию ближайшего пробела, в контексте общей задачи это также
        уникальный идентификатор
        Задача: обеспечить правильное разделение на блоки (не сечь слова)
        """

        idx = offset + uniqueid
        # Если мы в конце текста или уже стоим на пробеле
        if len(text) == idx or text[idx] == " ":
            # Отлично - верхнее значение подходит как уникальный идентификатор
            return uniqueid
        i = idx
        # Пока не спустились до смещения и по текущему расположению нет пробела
        while i >= offset and text[i] != " ":
            # Просто ищем подходящий индекс
            i -= 1
        # Если все-таки спустились до смещения
        if i <= offset:
            # Плохо - нет нужных пробелов - разрезать не получилось
            #   возвращаем верхнее значение - это единственное что мы можем сделать
            return uniqueid
        # Отлично - мы нашли нужный пробел, возвращаем разницу как уникальный
        #   идентификатор
        return i - offset

    def genUniqueIdsFree(self, text, segmentlen):
        """Метод ищет подходящие уникальные идентификаторы для разбития текста
        Вход: текст, предпочтительная длина блока
        Выход: список уникальных идентификаторов, по которым можно однозначно
            определить к какому именно тексту пришел ответ от сервиса Yandex SpeechKit
        Задача: построить список длин блоков (также являются уникальными идентификаторами)
        """

        retval = []
        length = len(text)
        # Вычисляем число сегментов, которые могли бы быть полными
        #   при таком расскладе реальное количество сегментов должно
        #   на 1 (len(all) // len(seg) + 1)
        numberofsegments = length // segmentlen
        offset = 0
        uniqueid = 0
        tail = 0
        tmpval = 0
        # Пока число уникальных ключей в ответе меньше чем число сегментов
        while len(retval) < numberofsegments:
            # Не использованую длину от предыдущего сегмента добавляем в новый
            uniqueid = segmentlen + tail
            # Ищем пробел
            tmpval = self.whereNearSpace(text, uniqueid, offset)
            # Запоминаем сколько пришлось отсечь
            tail = uniqueid - tmpval
            uniqueid = tmpval
            # Пока не подберем свободный уникальный идентификатор
            while not self.isUniqueFree(uniqueid):
                # BEG:DBG Плохой участок, не соответствует задаче - переписать
                #   Здесь должна быть обработка плохой ситуации, когда разрезать
                #   не удалось потому что не нашли нужный пробел
                if offset + uniqueid == length:
                    uniqueid += 1
                    continue
                # END:DBG
                # Смещаемся на 1, чтобы уйти с пробела, который нам не подходит
                uniqueid -= 1
                # Ищем следующий пробел
                tmpval = self.whereNearSpace(text, uniqueid, offset)
                # Учет отсеченного хвостика
                tail += uniqueid - tmpval
                uniqueid = tmpval
            # Отлично - уникальный идентификатор для блока подобран,
            #   добавляем его к ответу
            retval.append(uniqueid)
            # Смещаемся вперед
            offset += uniqueid
        # Если смещение стоит не в конце, значит у нас есть хвостик
        #   это тот самый неучтенный блок в выражении:
        #   numberofsegments = length // segmentlen
        if offset < length:
            # Добавляем его в список уникальных идентификаторов
            # DBG Не проверен на уникальность! - переписать
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
