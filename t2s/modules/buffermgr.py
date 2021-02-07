class BufferMsg(object):
    """Класс BufferMsg используется для хранения одного сообщения пользователя,
    и соответствуюшего ему списка данных о разбиении на блоки.

    Основное применение - хранение одного сообщения

    Атрибуты
    --------
    unqueids
        список данных о разбиении, а именно, размеров каждого блока, кроме того
        размеры блоков также являются специально подобранными уникальными
        идентификаторами блоков текста этого сообщения
    msg
        текст сообщения, который необходимо хранить

    Методы
    ------
    getUniqueIds
    getMsg
        методы для доступа к уникальным идентификаторам и сообщению

    Примечание
    ----------
    Методы доступа небезопасны, так как возвращают приватные поля,
    доступные для изменения
    """

    def __init__(self, uniqueids, msg):
        self.__uniqueids = uniqueids
        self.__buffer = msg

    def getUniqueIds(self):
        return self.__uniqueids

    def getMsg(self):
        return self.__buffer


class BufferMultiMsg(object):
    """Класс BufferMultiMsg используется для хранения нескольких сообщений
    пользователя, которые были получены до истечения таймаута и будут объединены
    в один аудио файл при генерации речи

    Основное применение - хранение сообщения, состоящего из нескольких одинарных

    Атрибуты
    --------
    пусто

    Методы
    ------
    pushMsg
        добавляет сообщение и данные о разбиении на блоки в список сообщений
    numberMessages
        возвращает количество одинарных сообщений
    getMessage
        возврашает сообщение по его идентификатору
    clear
        удаляет данные сообщений для экономии памяти
    """

    def __init__(self):
        self.__buffer = []

    def pushMsg(self, uniqueids, msg):
        self.__buffer.append(BufferMsg(uniqueids, msg))

    def numberMessages(self):
        return len(self.__buffer)

    def getMessage(self, msgid):
        return self.__buffer[msgid]

    def clear(self):
        self.__buffer.clear()


class BufferMgr(object):
    """Класс BufferMgr используется для хранения сообщений пользователя

    Основное применение - хранение сообщений, для отложенной обработки
    в частности для склеивания подряд идущих сообщений

    Атрибуты
    --------
    пусто

    Методы
    ------
    pushMsg
        размещает сообщение и данные о разбиении в буфер к мультисообщению
        соответствующему идентификатору асинхронной обработки
    getMultiMsg
        возвращает мультисообщение по идентификатору асинхронной обработки
    delMsg
        очищает мультисообщение для экономии памяти
    """

    def __init__(self):
        self.__tmpasyncid = -1
        self.__buffer = []

    def pushMsg(self, asyncid, uniqueids, msg):
        """Метод для размещения сообщения в буфер
        Вход: идентификатор асинхронной обработки, список данных о разбиении, сообщение
        Выход: пусто
        Задача: разместить сообщение в буфере
        """

        if self.__tmpasyncid < asyncid:
            self.__buffer.append(BufferMultiMsg())
            self.__tmpasyncid = asyncid
        self.__buffer[asyncid].pushMsg(uniqueids, msg)

    def getMultiMsg(self, asyncid):
        return self.__buffer[asyncid]

    def delMsg(self, asyncid):
        self.__buffer[asyncid].clear()
