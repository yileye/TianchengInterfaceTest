#coding=utf8
#######################################################
#filename:Interface_MQServer.py
#author:defias
#date:2016-1
#function: MQ Server
#######################################################
from Global import *
import pika
import ModMock
import TestCase
import threading
import CustomDataPg
import GoogleProtoBuffer
import json

class MQServer(object):
    '''
    MQ服务
    '''
    def __init__(self):
        self.ModMockO = ModMock.ModMock()
        self.PketO = CustomDataPg.ProtoPket()
        self.ProBufO = GoogleProtoBuffer.ProBuffer()

    def getMQMockDatai(self, identity_card, funcode):
        '''
        获得MQMock数据
        '''
        try:
            #获取用例文件Mock数据
            sheet, tid = self.ModMockO.getSheetId_from_identity_card(identity_card)
            MockData = TestCase.TestCaseXls.get_MockData(sheet, tid)
            PrintLog('info', '[%s] sheet: %s id: %s', threading.currentThread().getName(), sheet, tid)
            MockData = self.ModMockO.parseMockData(MockData)
            if MockData is False:
                PrintLog('info', '[%s] getMQMockData is Fail', threading.currentThread().getName())
                return None
            MQMockDate = MockData[1]
            PrintLog('info', '[%s] MQMockDate: %s ', threading.currentThread().getName(), MQMockDate)
            if MQMockDate == None:
                raise ValueError(u'MQMockDate is None')

            #确定DataKey
            DataKey = self.FunCode_DataKeyExchangeName[funcode][0]
            PrintLog('info', '[%s] DataKey: %s', threading.currentThread().getName(), DataKey)
            MQMockDatai = MQMockDate[DataKey]
            return json.dumps(MQMockDatai)
        except Exception as e:
            PrintLog('exception',e)
            return None

    def CallbackFunc(self, ch, method, properties, body):
        '''
        消息接收回调函数
        '''
        ExchangeName = method.exchange
        PrintLog('info', '[%s] CallbackFunc from ExchangeName: %s', threading.currentThread().getName(), ExchangeName)

        #解析body
        funcode,pdata,session_id = self.PketO.unpackPket(body)
        PrintLog('info', '[%s] 解包body结果: funcode: %s', threading.currentThread().getName(), funcode)

        response_topic, identity_card = self.ProBufO.Unserialize(pdata)
        PrintLog('info', '[%s] 解析body结果: response_topic: %s identity_card: %s', threading.currentThread().getName(), response_topic, identity_card)

        #获取响应数据
        MQMockDatai = self.getMQMockDatai(identity_card, funcode)
        PrintLog('info', '[%s] 获取响应数据: MQMockDatai: %s', threading.currentThread().getName(), MQMockDatai)

        if MQMockDatai != None:
            #构造body
            pbdata = self.ProBufO.Serialize(MQMockDatai)
            resp_body = self.PketO.packPket(pbdata, funcode, session_id)
            PrintLog('info', '[%s] 构造响应body完成!', threading.currentThread().getName())

            #发送
            ch.basic_publish(exchange=response_topic,
                        routing_key='',
                        body=resp_body)
            PrintLog('info', '[%s] 消息推送: [exchange]response_topic: %s\n', threading.currentThread().getName(), response_topic)

    def Start(self):
        '''
        启动MQ服务
        '''
        try:
            # 登录MQ建立连接
            MQinfo = self.ModMockO.getRuncaseEnvironment_MQ()
            MQhost, MQport, MQusername, MQpasswd, MQvhost = MQinfo
            credentials = pika.PlainCredentials(MQusername, MQpasswd)           #登录
            parameters = pika.ConnectionParameters(MQhost, MQport, MQvhost, credentials)          #连接
            self.connection = pika.BlockingConnection(parameters)
            self.channel = self.connection.channel()

            # 消息订阅
            self.FunCode_DataKeyExchangeName = self.ModMockO.get_FunCode_DataKeyExchangeName()
            ExchangeNamelist = [x[1] for x in self.FunCode_DataKeyExchangeName.values()]
            ExchangeNamelist = list(set(ExchangeNamelist))
            PrintLog('info', '[%s] 消息订阅: ExchangeNamelist: %s', threading.currentThread().getName(), ExchangeNamelist)
            for ExchangeName in ExchangeNamelist:
                QueueName = ExchangeName + '_AUTOTEST'
                self.channel.queue_delete(queue=QueueName) #先删除保证不受残留消息的影响
                self.channel.queue_declare(queue=QueueName, durable=False) #定义消息队列
                self.channel.queue_bind(exchange=ExchangeName, queue=QueueName) #绑定到交换机
                self.channel.basic_consume(self.CallbackFunc, queue=QueueName, no_ack=True)  #消息订阅
            PrintLog('info', '[%s] MQ cusume is running....', threading.currentThread().getName())
            self.channel.start_consuming()
        except Exception as e:
            PrintLog('exception',e)
