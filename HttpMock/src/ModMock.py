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

    def getRuncaseEnvironment_HTTP(self):
        '''
        获取环境信息:HTTP信息
        '''
        HTTPhost = Config.ConfigIni.get_TestEnvironment_Info('DEFAULT', 'host')
        HTTPport = Config.ConfigIni.get_TestEnvironment_Info('DEFAULT', 'port')
        HTTPinfo = (HTTPhost, int(HTTPport))
        return HTTPinfo

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

    def HttpData_Key2ID(self, Key):
        '''
        HttpData: 通过Key获取ID
        '''
        HttpData_ID_Key = eval(HttpMEMdata.getvalue())
        HttpData_ID_Keyi = filter(lambda x: x[1]==int(Key),HttpData_ID_Key.items())
        IDs =  [x[0] for x in HttpData_ID_Keyi]
        if len(IDs) == 0:
            HttpData_ID_Keyi = filter(lambda x: x[1]=='default',HttpData_ID_Key.items())
            IDs =  [x[0] for x in HttpData_ID_Keyi]
        return IDs[0]

    def HttpData_ID_Key(self, IDs):
        '''
        HttpData: 所有ID和Key
        '''
        ID_Key = {}
        for ID in IDs:
            Key = MockData.MockDataXls.get_Key(ID)
            ID_Key[ID] = Key
        #查重
        if len(ID_Key.values()) != len(set(ID_Key.values())):
            PrintLog('debug', 'HttpData: ID_Key中存在重复数据: %s', ID_Key)
            return False
        return ID_Key
