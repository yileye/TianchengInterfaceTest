#coding=utf8
#######################################################
#filename:Interface_Mock.py
#author:defias
#date:2016-1
#function: Mock Thread
#######################################################
from Global import *
import Global
import Interface_Driver
import Interface_MQServer
import Interface_HttpServer
import threading

def StartMockServer(MockData, ModO, TestEnvironment):
    '''
    启动Mock服务子线程-入口
    '''
    try:
        StartResult = {}
        MockDataDict = ModO.parseMockDataForDriver(MockData)
        PrintLog('debug', '[%s] MockData解析结果MockDataDict: %s', threading.currentThread().getName(), MockDataDict)

        #启动MQ MOCK服务
        if 'MQMOCK' in MockDataDict:
            #获取数据
            MQMockData = MockDataDict['MQMOCK']
            if MQMockData != {}:
                MQinfo = ModO.getRuncaseEnvironment_MQ(TestEnvironment)

                #开启线程
                PrintLog('debug', '[%s] 开启MQMockThread线程: MQMockData:%s\nMQinfo:%s', threading.currentThread().getName(), MQMockData, MQinfo)
                MQMockThreadO = MQMockThread('MQMockThread', MQMockData, MQinfo)
                MQMockThreadO.setDaemon(True)
                MQMockThreadO.start()
                StartResult['MQMOCK'] = MQMockThreadO

        #启动HTTP MOCK服务
        if 'HTTPMOCK' in MockDataDict:
            HTTPMockData = MockDataDict['HTTPMOCK']
            if HTTPMockData != {}:
                HTTPinfo = ModO.getRuncaseEnvironment_HTTP(TestEnvironment)
                #开启线程
                PrintLog('debug', '[%s] 开启HTTPMockThread线程: HTTPMockData: %s\nHTTPinfo:%s', threading.currentThread().getName(), HTTPMockData, HTTPinfo)
                HTTPMockThreadO = HTTPMockThread('HTTPMockThread', HTTPMockData, HTTPinfo)
                HTTPMockThreadO.setDaemon(True)
                HTTPMockThreadO.start()
                StartResult['HTTPMOCK'] = HTTPMockThreadO

        #数据插入INSERT TABLE服务
        if 'TABLE' in MockDataDict:
            TABLEData = MockDataDict ['TABLE']
            if TABLEData != {}:
                TABLEinfo = ModO.getRuncaseEnvironment_TABLE(TestEnvironment)

                #开启线程
                PrintLog('debug', '[%s] 开启TABLEThread线程:TABLEData:%s\nTABLEinfo:%s', threading.currentThread().getName(), TABLEData, TABLEinfo)
                TABLEThreadO = TABLEThread('TABLEThread', TABLEData, TABLEinfo)
                TABLEThreadO.setDaemon(True)
                TABLEThreadO.start()
                StartResult['TABLE'] = TABLEThreadO
        return StartResult
    except Exception as e:
        PrintLog('exception', e)
        return False


class MQMockThread(threading.Thread):
    '''
    MQmock服务子线程类
    '''
    def __init__(self, tdname, MQMockData, MQinfo):
        threading.Thread.__init__(self, name=tdname)
        self.MQServerO = Interface_MQServer.MQServer(MQMockData, MQinfo)
        self.connection = self.MQServerO.connection

    def run(self):
        try:
            PrintLog('debug', '[%s] Start MQServer', threading.currentThread().getName())
            self.MQServerO.Start()
        except Exception as e:
            Global.isMQMock = 'except'
            PrintLog('exception',e)


class HTTPMockThread(threading.Thread):
    '''
    HTTPmock服务子线程类
    '''
    def __init__(self, tdname, HTTPMockData, HTTPinfo):
        threading.Thread.__init__(self, name=tdname)
        self.HTTPServerO = Interface_HttpServer.HttpServer(HTTPMockData, HTTPinfo)
        self.myhttpd = self.HTTPServerO.myhttpd

    def run(self):
        try:
            PrintLog('debug', '[%s] Start HTTPServer', threading.currentThread().getName())
            self.HTTPServerO.Start()
        except Exception as e:
            Global.isHTTPMock = 'except'
            PrintLog('exception',e)

class TABLEThread(threading.Thread):
    '''
    插数据子线程类
    '''
    def __init__(self, tdname, TABLEData, TABLEinfo):
        threading.Thread.__init__(self, name=tdname)
        self.TABLEData = TABLEData
        self.TABLEinfo = TABLEinfo
        self.DriverO = Interface_Driver.Interface_DoData(self.TABLEinfo)

    def parseTABLEData(self, TABLEData):
        '''
        解析数据为: [(table, fieldlist, valuelist), (table, fieldlist, valuelist), ...]
        '''
        params_result = []
        tables = TABLEData.keys()
        for table in tables:
            fields = TABLEData[table].keys()
            values = TABLEData[table].values()
            params_result.append((table, fields, values))
        return params_result

    def run(self):
        try:
            parseTABLEData = self.parseTABLEData(self.TABLEData)
            PrintLog('debug', '[%s] 插数据:parseTABLEData:%s', threading.currentThread().getName(), parseTABLEData)
            DriverResult = DriverO.insert(parseTABLEData)    #插数据
            if DriverResult is not True:
                raise MyError('TABLE: Insert TABLEData Error')
            Global.isTABLE = True
        except Exception as e:
            Global.isTABLE = 'except'
            PrintLog('exception',e)
