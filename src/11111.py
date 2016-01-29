 def StartMock(self, MockData, ModO, TestEnvironment):
        '''
        开启Mock线程
        '''
        if MockData != '':
            PrintLog('debug', '[%s] 启动MOCK服务子线程: MockData: %s\nTestEnvironment: %s', threading.currentThread().getName(), MockData, TestEnvironment)
            StartResult = Interface_Mock.StartMockServer(MockData, ModO, TestEnvironment)
            PrintLog('debug', '[%s] 启动MOCK服务子线程完成: StartResult: %s', threading.currentThread().getName(), StartResult)
            if StartResult is False:
                PrintLog('debug', '[%s] 启动MOCK服务子线程时出现异常', threading.currentThread().getName())
                return False

            #确保Mock子线程服务开启
            if 'TABLE' in StartResult:
                while not Global.isTABLE:
                    PrintLog('debug', '[%s] sleep isTABLE...', threading.currentThread().getName())
                    time.sleep(0.5)
                PrintLog('debug', '[%s] sleep isTABLE end', threading.currentThread().getName())

                if Global.isTABLE == 'except':
                    PrintLog('debug', '[%s] TABLEThread线程异常', threading.currentThread().getName())
                    return False
                elif Global.isTABLE is True:
                    Global.isTABLE = False
                    PrintLog('debug', '[%s] TABLEThread线程服务完成', threading.currentThread().getName())

            if 'MQMOCK' in StartResult:
                while not Global.isMQMock:
                    PrintLog('debug', '[%s] sleep isMQMock...', threading.currentThread().getName())
                    time.sleep(0.5)
                PrintLog('debug', '[%s] sleep isMQMock end', threading.currentThread().getName())

                if Global.isMQMock == 'except':
                    PrintLog('debug', '[%s] MQMockThread线程异常', threading.currentThread().getName())
                    return False
                elif Global.isMQMock is True:
                    Global.isMQMock = False
                    PrintLog('debug', '[%s] MQMockThread线程服务开启', threading.currentThread().getName())

            if 'HTTPMOCK' in StartResult:
                while not Global.isHTTPMock:
                    PrintLog('debug', '[%s] sleep isHTTPMock...', threading.currentThread().getName())
                    time.sleep(0.5)
                PrintLog('debug', '[%s] sleep isHTTPMock end', threading.currentThread().getName())

                if Global.isHTTPMock == 'except':
                    PrintLog('debug', '[%s] HTTPMockThread线程异常', threading.currentThread().getName())
                    return False
                elif Global.isHTTPMock is True:
                    Global.isHTTPMock = False
                    PrintLog('debug', '[%s] HTTPMockThread线程服务开启', threading.currentThread().getName())
            time.sleep(10)
            return StartResult

    def EndMock(self, MockData, StartResult):
        '''
        结束Mock线程
        '''
        if MockData != '' and StartResult != {} and StartResult != False:
            PrintLog('debug', '[%s] EndMock sleep...', threading.currentThread().getName())
            time.sleep(5)   #延时一段时间，测试操作成功后，不代表第三方服务就可以结束，这里通过延时一固定时间提供第三方服务，并不是非常可靠的做法
            PrintLog('debug', '[%s] 结束MOCK服务子线程， StartResult: %s', threading.currentThread().getName(), StartResult)
            if 'HTTPMOCK' in StartResult:
                HTTPMockThreadO = StartResult['HTTPMOCK']
                try:
                    HTTPMockThreadO.myhttpd.stop_server()
                except:
                    pass
                    PrintLog('debug', '[%s]  HTTPMockThreadO.myhttpd.stop_server() end', threading.currentThread().getName())
                while HTTPMockThreadO.isAlive():
                    time.sleep(1)
                PrintLog('debug', '[%s] HTTPMockThreadO线程服务结束', threading.currentThread().getName())

            if 'MQMOCK' in StartResult:
                MQMockThreadO = StartResult['MQMOCK']
                try:
                    MQMockThreadO.connection.close()
                except:
                    pass
                    PrintLog('debug', '[%s]  MQMockThreadO.connection.close() end', threading.currentThread().getName())
                while MQMockThreadO.isAlive():
                    time.sleep(1)
                PrintLog('debug', '[%s] MQMockThreadO线程服务结束', threading.currentThread().getName())

            if 'TABLE' in StartResult:
                TABLEThreadO = StartResult['TABLE']
                if TABLEThreadO.isAlive():
                    TABLEThreadO.join()
                PrintLog('debug', '[%s] TABLEThreadO线程服务结束', threading.currentThread().getName())










    def parseMockDataForDriver(self, MockData):
        '''
        解析MockData
        '''
        try:
            if MockData == '':
                raise ValueError
            else:
                MockDataDict = json.loads(MockData)
            return MockDataDict
        except Exception as e:
            PrintLog('exception',e)
            return False












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








 # if type(expvalue[key]) is dict:
                        #     for kk in expvalue[key]:
                        #         assert kk in de_resultDict[key], u'检查BASE64加密字段: %s字段中:%s字段中无:%s字段' % (fields[i], key, kk)
                        #         if kk == 'fanyilist':
                        #             PrintLog('debug', '[%s] _检查BASE64加密字段数据: de_resultDict[%s][%s]: %s\nexpvalue[%s][%s]: %s', threading.currentThread().getName(), key, kk, de_resultDict[key][kk], key, kk, expvalue[key][kk])
                        #             self.check_fanyilist(de_resultDict[key][kk], expvalue[key][kk])
                        #         elif type(expvalue[key][kk]) is dict:
                        #             PrintLog('debug', '[%s] _检查BASE64加密字段数据: de_resultDict[%s][%s]: %s\nexpvalue[%s][%s]: %s', threading.currentThread().getName(), key, kk, de_resultDict[key][kk], key, kk, expvalue[key][kk])
                        #             assert json_tools.diff(json.dumps(de_resultDict[key][kk]), json.dumps(expvalue[key][kk])) == [], u'_检查BASE64加密字段: %s字段中:%s字段中:%s字段数据与期望数据不一致' % (fields[i], key, kk)
                        #         else:
                        #             PrintLog('debug', '[%s] 检查BASE64加密字段数据: de_resultDict[%s][%s]: %s\nexpvalue[%s][%s]: %s', threading.currentThread().getName(), key, kk, de_resultDict[key][kk], key, kk, expvalue[key][kk])
                        #             assert de_resultDict[key][kk] == expvalue[key][kk], u'检查BASE64加密字段: %s字段中:%s字段中:%s字段中数据与期望数据不一致' % (fields[i], key, kk)

