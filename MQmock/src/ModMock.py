#coding=utf8
#######################################################
#filename: ModMock.py
#author: defias
#date: 2016-1
#function: Mock相关
#######################################################
from Global import *
import Config
import json
import MockData

class ModMock(object):
    def __init__(self):
        pass

    def getRuncaseEnvironment_MQ(self):
        '''
        获取环境信息:MQ信息
        '''
        MQhost = Config.ConfigIni.get_TestEnvironment_Info('DEFAULT', 'MQhost')
        MQport = Config.ConfigIni.get_TestEnvironment_Info('DEFAULT', 'MQport')
        MQusername = Config.ConfigIni.get_TestEnvironment_Info('DEFAULT', 'MQusername')
        MQpasswd = Config.ConfigIni.get_TestEnvironment_Info('DEFAULT', 'MQpasswd')
        MQvhost = Config.ConfigIni.get_TestEnvironment_Info('DEFAULT', 'MQvhost')
        MQinfo =  (MQhost, int(MQport), MQusername, MQpasswd, MQvhost)
        return MQinfo

    def get_FunCode_DataKeyExchangeName(self):
        '''
        获取Functioncode-queue名对应信息
        '''
        FunCode_DataKeyExchangeName = Config.ConfigIni.get_FunCode_DataKeyExchangeName()
        return eval(FunCode_DataKeyExchangeName)

    def parseMockData(self, MockData):
        '''
        解析MockData
        '''
        try:
            if MockData != '' and MockData is not False:
                MockDataDict = json.loads(MockData)
            else:
                raise ValueError

            return MockDataDict
        except Exception as e:
            PrintLog('exception',e)
            return False

    def MQData_Key2ID(self, Key):
        '''
        MQData: 通过Key获取ID
        '''
        MQData_ID_Key = eval(MQMEMdata.getvalue())
        MQData_ID_Keyi = filter(lambda x: x[1]==unicode(Key),MQData_ID_Key.items())
        IDs =  [x[0] for x in MQData_ID_Keyi]
        if len(IDs) == 0:
            MQData_ID_Keyi = filter(lambda x: x[1]=='default',MQData_ID_Key.items())
            IDs =  [x[0] for x in MQData_ID_Keyi]
        return IDs[0]

    def MQData_ID_Key(self, IDs):
        '''
        MQData: 所有ID和Key
        '''
        ID_Key = {}
        for ID in IDs:
            Key = MockData.MockDataXls.get_Key(ID)
            ID_Key[ID] = Key
        #查重
        if len(ID_Key.values()) != len(set(ID_Key.values())):
            PrintLog('debug', 'MQData: ID_Key中存在重复数据: %s', ID_Key)
            return False
        return ID_Key
