#coding=utf8
#######################################################
#filename:Interface_ProtoBuffer.py
#author:defias
#date:2016-1
#function: google proto buffer
#######################################################
from Global import *
import GoogleProtoBuf
import struct
import json
import threading


class ProtoBuffer(object):
    '''
    google buffer数据协议
    '''
    def __init__(self, MQMockData, Key_FunCodeQueueNameDict):
        self.MQMockData = MQMockData
        self.Key_FunCodeQueueNameDict = Key_FunCodeQueueNameDict
        self.ProtoPketO = ProtoPket()

    def parsebody(self, body):
        '''
        解析body 返回FunCode和Response_Topic
        '''
        #解包
        FunCode, PData = self.ProtoPketO.unpackPket(body)
        PrintLog('debug', '[%s] body解包结果: FunCode: %s PData: %s', threading.currentThread().getName(), FunCode, PData)

        #反序列化
        user_verification_ask = GoogleProtoBuf.QDP_main_frame_pb2.user_verification_ask()
        user_verification_ask.ParseFromString(PData)
        Response_Topic = user_verification_ask.ask_header.response_topic
        PrintLog('debug', '[%s] 反序列化结果: Response_Topic: %s', threading.currentThread().getName(), Response_Topic)

        return FunCode, Response_Topic

    def getMessages(self, FunCode):
        '''
        封装待发送的数据Messages
        '''
        #获取待发送数据
        FunCode_Key = {self.Key_FunCodeQueueNameDict[x][0]:x for x in self.Key_FunCodeQueueNameDict}
        Datakey = FunCode_Key[FunCode]
        Data = self.MQMockData[Datakey]
        PrintLog('debug', '[%s] 读取待发送数据: Data: %s', threading.currentThread().getName(), Data)

        #序列化
        PrintLog('debug', '[%s] --------开始序列化-----------', threading.currentThread().getName())
        user_verification_ans = GoogleProtoBuf.QDP_main_frame_pb2.user_verification_ans()
        user_verification_ans.platform_type = GoogleProtoBuf.QDP_main_frame_pb2.other_platform.unknown_platform
        errorinfo = user_verification_ans.error.add()
        errorinfo.error_code = GoogleProtoBuf.common_pb2.ASK_SUCCEED
        user_verification_ans.json_ans = bytes(json.dumps(Data))
        errorinfo.SerializeToString()
        user_verification_ans_str = user_verification_ans.SerializeToString()
        PrintLog('debug', '[%s] -------序列化结果: user_verification_ans_str: %s ', threading.currentThread().getName(), user_verification_ans_str)

        #打包
        messages = self.ProtoPketO.packPket(user_verification_ans_str, FunCode)
        PrintLog('debug', '[%s] -------打包结果: messages: %s ', threading.currentThread().getName(), messages)
        return messages

class ProtoPket(object):
    '''
    自定义数据包协议
    '''
    MSGPPK_BEGIN = chr(0xff)
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

    def packPket(self, pdata, funcode):
        '''
        打包
        '''
        self.MSGPPK_PDATA = pdata
        self.MSGPPK_DATA_LEN = len(pdata)
        outpdata_formt = '<BIIHHBQIIIIIII'
        outpdata_len = struct.calcsize(outpdata_formt)
        self.MSGPPK_PKET_LEN = outpdata_len + MSGPPK_DATA_LEN
        self.MSGPPK_SESSION_ID = 201601 + random.randint(1,1000)
        self.MSGPPK_FUNCODE = funcode
        msg_formt = '<BIIHHBQIIIIII%dsI' % MSGPPK_DATA_LEN

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
        return funcode,pdata
