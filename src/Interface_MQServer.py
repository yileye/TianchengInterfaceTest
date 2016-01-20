#coding=utf8
#######################################################
#filename:Interface_MQServer.py
#author:defias
#date:2016-1
#function: MQ Server
#######################################################
from Global import *
import Global
import pika
import Config
import Interface_ProtoBuffer
import threading

class MQServer(object):
    '''
    MQ服务
    '''
    def __init__(self, MQMockData, MQinfo):
        self.MQMockData = MQMockData
        self.MQinfo = MQinfo
        self.Key_FunCodeQueueNameDict = eval(Config.ConfigIni.get_QueueName())    #DataKey-(FunCode, QueueName)配置
        self.ProtoBufferO = Interface_ProtoBuffer.ProtoBuffer(self.MQMockData, self.Key_FunCodeQueueNameDict)   #数据协议

        #登录MQ建立连接
        MQhost, MQport, MQusername, MQpasswd, MQvhost = self.MQinfo
        credentials = pika.PlainCredentials(MQusername, MQpasswd)           #登录
        parameters = pika.ConnectionParameters(MQhost, MQport, MQvhost, credentials)          #连接
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()

    def getQueueName(self, item):
        '''
        根据MQmock数据key获取MQ队列名
        '''
        if item in self.Key_FunCodeQueueNameDict:
            return self.Key_FunCodeQueueNameDict[item][2]
        else:
            return False

    def CallbackFunc(self, ch, method, properties, body):
        '''
        消息接收回调函数
        '''
        #解析body
        print 'CallbackFunc.........'
        FunCode, Response_Topic = self.ProtoBufferO.parsebody(body)
        PrintLog('debug', '[%s] 解析body结果: FunCode: %s Response_Topic: %s', threading.currentThread().getName(), FunCode, Response_Topic)

        #构造Messages
        Messages = self.ProtoBufferO.getMessages(FunCode)

        #发送Messages
        Response_exchange = '???'
        PrintLog('debug', '[%s] 消息推送: Response_exchange: %s Response_Topic: %s', threading.currentThread().getName(), Response_exchange, Response_Topic)
        self.channel.basic_publish(exchange=Response_exchange, routing_key=Response_Topic, body=Messages)

    def Start(self):
        '''
        启动
        '''
        for item in self.MQMockData.keys():
            QueueName = self.getQueueName(item)
            if QueueName is False:
                raise MyError('MQMOCK: Get QueueName False')
            PrintLog('debug', '[%s] 消息订阅: QueueName: %s', threading.currentThread().getName(), QueueName)
            self.channel.basic_consume(self.CallbackFunc, queue=QueueName, no_ack=True)  #消息订阅
        PrintLog('debug', '[%s] MQ cusume is running....', threading.currentThread().getName())
        Global.isMQMock = True
        self.channel.start_consuming()
