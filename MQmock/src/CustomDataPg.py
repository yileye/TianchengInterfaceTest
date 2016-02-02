#coding=utf8
#######################################################
#filename: CustomDataPg.py
#author: defias
#date: 2016-1
#function: Custom Data Package Proto
#######################################################
import struct
import random


class ProtoPket(object):
    '''
    自定义数据包协议
    '''
    MSGPPK_BEGIN = int(0xff)
    MSGPPK_PKET_LEN = 0
    MSGPPK_FUNCODE = 0
    MSGPPK_BIG_VERSION = 0
    MSGPPK_SMALL_VERSION = 0
    MSGPPK_ENCRYPT_MODE = 0
    MSGPPK_SESSION_ID = 0
    MSGPPK_TO_ID = 0
    MSGPPK_FROM_ID = 0
    MSGPPK_APP_ID = 0
    MSGPPK_RESERVER_FIELD1 = 0
    MSGPPK_RESERVER_FIELD2 = 0
    MSGPPK_DATA_LEN = 0
    MSGPPK_PDATA = 0
    MSGPPK_PK_CRC = 0

    def __init__(self):
        pass

    def packPket(self, pdata, funcode, session_id):
        '''
        打包
        '''
        self.MSGPPK_PDATA = pdata
        self.MSGPPK_DATA_LEN = len(pdata)
        outpdata_formt = '<BIIHHBQIIIIIII'
        outpdata_len = struct.calcsize(outpdata_formt)
        self.MSGPPK_PKET_LEN = outpdata_len + self.MSGPPK_DATA_LEN
        self.MSGPPK_SESSION_ID = session_id
        self.MSGPPK_FUNCODE = funcode
        msg_formt = '<BIIHHBQIIIIII%dsI' % self.MSGPPK_DATA_LEN

        messages = struct.pack(msg_formt, self.MSGPPK_BEGIN, self.MSGPPK_PKET_LEN, self.MSGPPK_FUNCODE, self.MSGPPK_BIG_VERSION, self.MSGPPK_SMALL_VERSION,
                                    self.MSGPPK_ENCRYPT_MODE, self.MSGPPK_SESSION_ID, self.MSGPPK_TO_ID, self.MSGPPK_FROM_ID, self.MSGPPK_APP_ID,
                                    self.MSGPPK_RESERVER_FIELD1, self.MSGPPK_RESERVER_FIELD2, self.MSGPPK_DATA_LEN, self.MSGPPK_PDATA, self.MSGPPK_PK_CRC)
        return messages

    def unpackPket(self, messages):
        '''
        解包
        '''
        msg_len = len(messages)
        outpdata_formt = '<BIIHHBQIIIIIII'
        outpdata_len = struct.calcsize(outpdata_formt)
        pdata_len = msg_len - outpdata_len
        msg_formt = '<BIIHHBQIIIIII%dsI' % pdata_len
        msg = struct.unpack(msg_formt, messages)
        funcode = msg[2]
        pdata = msg[-2]
        session_id = msg[6]
        return funcode, pdata, session_id
