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
import MockData
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

    def getMQMockDatai(self, Key, funcode):
        '''
        获得MQMock数据
        '''
        try:
            #获取用例文件Mock数据
            ID = self.ModMockO.MQData_Key2ID(Key)
            PrintLog('debug', '[MQServer] ID: %s', ID)
            MQMockDate = MockData.MockDataXls.get_MockData(ID)
            MQMockDate = self.ModMockO.parseMockData(MQMockDate)
            if MQMockDate is False:
                PrintLog('debug', '[MQServer] getMQMockDatai is Fail')
                return None
            PrintLog('debug', '[MQServer] MQMockDate: %s ',  MQMockDate)

            #确定DataKey
            DataKey = self.FunCode_DataKeyExchangeName[funcode][0]
            PrintLog('debug', '[MQServer] DataKey: %s',  DataKey)
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
        PrintLog('debug', '[MQServer] CallbackFunc from ExchangeName: %s',  ExchangeName)

        #解析body
        funcode,pdata,session_id = self.PketO.unpackPket(body)
        PrintLog('debug', '[MQServer] 解包body结果: funcode: %s',  funcode)

        response_topic, identity_card = self.ProBufO.Unserialize(pdata)
        PrintLog('debug', '[MQServer] 解析body结果: response_topic: %s identity_card: %s',  response_topic, identity_card)

        #获取响应数据
        MQMockDatai = self.getMQMockDatai(identity_card, funcode)
        PrintLog('debug', '[MQServer] 获取响应数据: MQMockDatai: %s',  MQMockDatai)

        if MQMockDatai != None:
            #构造body
            pbdata = self.ProBufO.Serialize(MQMockDatai)
            resp_body = self.PketO.packPket(pbdata, funcode, session_id)
            PrintLog('debug', '[MQServer] 构造响应body完成!')

            #发送
            ch.basic_publish(exchange=response_topic,
                        routing_key='',
                        body=resp_body)
            PrintLog('debug', '[MQServer] 消息推送: [exchange]response_topic: %s\n',  response_topic)

    def run(self):
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
            PrintLog('debug', '[MQServer] 消息订阅: ExchangeNamelist: %s',  ExchangeNamelist)
            for ExchangeName in ExchangeNamelist:
                QueueName = ExchangeName + '_AUTOTEST'
                self.channel.queue_delete(queue=QueueName) #先删除保证不受残留消息的影响
                self.channel.queue_declare(queue=QueueName, durable=False) #定义消息队列
                self.channel.queue_bind(exchange=ExchangeName, queue=QueueName) #绑定到交换机
                self.channel.basic_consume(self.CallbackFunc, queue=QueueName, no_ack=True)  #消息订阅
            PrintLog('debug', '[MQServer] MQ cusume is running....')
            self.channel.start_consuming()
        except Exception as e:
            PrintLog('exception',e)
