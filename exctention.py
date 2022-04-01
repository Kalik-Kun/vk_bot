from enum import Enum


class BotErrClass:
    def __init__(self, text='unknown', error_number=0, other=None):
        if other is None:
            self.text = text
            self.err_num = error_number
        else:
            self.text = other.text
            self.err_num = other.err_num

    def __str__(self):
        return "Code Error: {},  Message_error: {}".format(self.err_num, self.text)

    def __repr__(self):
        return "Code Error: {},  Message_error: {}".format(self.err_num, self.text)


class BotException(Exception):
    def __init__(self, other=None):
        self.error = BotErrClass(other=other.value)

    def __str__(self):
        return "Code Error: {},  Message_error: {}".format(self.error.err_num, self.error.text)


class EnumBotErrors(Enum):
    UNKNOWN_ERROR = BotErrClass()
    DONT_FIND_SYMB = BotErrClass(text='Symbol could not be found', error_number=1)
    ERROR_CONNECT_SERVER_MAX_TRY = BotErrClass(text='Server could not connect to vk server\n'
                                                    'Max attempts were used', error_number=2)
    SERVER_SHUTDOWN = BotErrClass(text='SERVER SHUTDOWN', error_number=2)