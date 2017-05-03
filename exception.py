# -*- coding: utf-8 -*-


EXCEPTION_MESSAGE = {
    40000: '调用百度地图API失败',
    40001: '在地图上找不到该地址',
}


class TException(Exception):

    def __init__(self, code):
        message = EXCEPTION_MESSAGE.get(code, None)
        super(TException, self).__init__(message)


class AddressException(TException):
    pass