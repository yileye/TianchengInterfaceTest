#coding=utf8
#######################################################
#filename:Interface_DriverEngine.py
#author:defias
#date:2015-7
#function:Driver Engine
#######################################################
from Global import *
import threading
import TestCase
import Interface_Driver
import ModUPS
import ModUPSLabel
import ModUBAS
import ModAFP
import ModCCS
import Interface_Mock
import time


class Interface_DriverEngine():
    '''
    执行单条测试用例
    '''
    def __init__(self):
        global taskassert_queue
        self.taskassert_queue = taskassert_queue
        self.TestCaseO = TestCase.TestCaseXls

    def StartMock(self, MockData, ModO, TestEnvironment):
        '''
        开启Mock线程
        '''
        if MockData != '':
            PrintLog('debug', '[%s] 启动MOCK服务子线程， MockData: %s', threading.currentThread().getName(), MockData)
            StartResult = Interface_Mock.StartMockServer(MockData, ModO, TestEnvironment)
            if StartResult is False:
                return False

            #确保数据插入子线程结束
            if 'TABLE' in StartResult:
                TABLEThreadO = StartResult['TABLE']
                if TABLEThreadO.isAlive():
                    PrintLog('debug', '[%s] 等待TABLEThreadO线程完成...', threading.currentThread().getName())
                    TABLEThreadO.join()
            return StartResult
        return False

    def EndMock(self, MockData, StartResult):
        '''
        结束Mock线程
        '''
        if MockData != '':
            PrintLog('debug', '[%s] 结束MOCK服务子线程， StartResult: %s', threading.currentThread().getName(), StartResult)
            if 'MQMOCK' in StartResult:
                MQMockThreadO = StartResult['MQMOCK']
                if MQMockThreadO.isAlive():
                    PrintLog('debug', '[%s] 结束MQMockThreadO线程', threading.currentThread().getName())
                    MQMockThreadO.connection.close()

            if 'HTTPMOCK' in StartResult:
                HTTPMockThreadO = StartResult['HTTPMOCK']
                if HTTPMockThreadO.isAlive():
                    PrintLog('debug', '[%s] 结束HTTPMockThreadO线程', threading.currentThread().getName())
                    HTTPMockThreadO.myhttpd.socket.close()

    def RunUBASCase(self, sheet, testid, TestData, TestEnvironment):
        '''
        运行数据回流接口用例
        '''
        ModUBASO = ModUBAS.ModUBAS()
        dbinfo = ModUBASO.getRuncaseEnvironment_db(TestEnvironment)
        url = ModUBASO.getRuncaseEnvironment_Url(TestEnvironment)
        headers = ModUBASO.getRuncaseEnvironment_Headers(TestEnvironment)

        #读取超时时间
        timeouttask = ModUBASO.getRuncaseEnvironment_Timeouttask(TestEnvironment)
        timeoutdelay = 0

        #获取待插入数据前表的maxid
        Expectation = self.TestCaseO.get_Expectation(sheet, testid)
        TableList = ModUBASO.parseExpForDriver(Expectation)
        if TableList is False:
            return False
        DriverOO = Interface_Driver.Interface_DoData(dbinfo)
        TableMaxid = DriverOO.getTableMaxid(TableList)

        #驱动执行获得response
        PrintLog('debug', '[%s] 驱动执行:headers:%s TestData:%s', threading.currentThread().getName(), headers, TestData)
        DriverO = Interface_Driver.Interface_Http(url)
        DriverResult = DriverO.post(headers, TestData)  #执行用例
        PrintLog('debug', '[%s] 执行结果:DriverResult:%s', threading.currentThread().getName(), DriverResult)

        #装载任务参数
        if DriverResult is False:
            return False
        taskargs = DriverResult,TableMaxid
        return timeouttask, timeoutdelay, taskargs

    def RunUPSCase(self, sheet, testid, TestData, TestEnvironment):
        '''
        运行用户画像接口用例
        '''
        ModUPSO = ModUPS.ModUPS()
        url = ModUPSO.getRuncaseEnvironment_Url(TestEnvironment)
        headers = ModUPSO.getRuncaseEnvironment_Headers(TestEnvironment)

        #读取超时时间
        timeouttask = ModUPSO.getRuncaseEnvironment_Timeouttask(TestEnvironment)
        timeoutdelay = 0

        #驱动执行获得返回的响应
        PrintLog('debug', '[%s] 驱动执行:headers:%s TestData:%s', threading.currentThread().getName(), headers, TestData)
        DriverO = Interface_Driver.Interface_Http(url)
        DriverResult = DriverO.post(headers, TestData)  #执行用例
        PrintLog('debug', '[%s] 执行结果:DriverResult:%s', threading.currentThread().getName(), DriverResult)

        #装载任务参数
        if DriverResult is False:
            return False
        taskargs = DriverResult
        return timeouttask, timeoutdelay, taskargs

    def RunUPSLabelCase(self, sheet, testid, TestData, TestEnvironment):
        '''
        运行用户画像标签用例
        '''
        ModUPSLabelO = ModUPSLabel.ModUPSLabel()
        dbinfo = ModUPSLabelO.getRuncaseEnvironment_Userdb(TestEnvironment)
        function = ModUPSLabelO.DriverCbFunction

        #读取超时时间
        timeouttask = ModUPSLabelO.getRuncaseEnvironment_Timeouttask_label(TestEnvironment)

        #读取延时时间
        Expectation = self.TestCaseO.get_Expectation(sheet, testid)
        parseRt = ModUPSLabelO.parseExpForDriver(Expectation)
        if parseRt is True:
            timeoutdelay = ModUPSLabelO.getRuncaseEnvironment_Timeoutdelay_label(TestEnvironment)
        else:
            timeoutdelay = 0

        #测试数据解析
        TestData = ModUPSLabelO.parseParamsForDriver(TestData)

        #驱动执行获得返回的唯一userid
        PrintLog('debug', '[%s] 驱动执行:TestData:%s CbFunction:%s', threading.currentThread().getName(), TestData, function.__name__)
        DriverO = Interface_Driver.Interface_DoData(dbinfo)
        DriverResult = DriverO.insert(TestData, function)    #执行用例
        PrintLog('debug', '[%s] 执行结果:DriverResult:%s', threading.currentThread().getName(), DriverResult)

        #装载任务参数
        if DriverResult is False:
            return False
        taskargs = DriverResult
        return timeouttask, timeoutdelay, taskargs

    def RunAFPCase(self, sheet, testid, TestData, TestEnvironment, MockData):
        '''
        运行反欺诈接口用例
        '''
        ModAFPO = ModAFP.ModAFP()
        url = ModAFPO.getRuncaseEnvironment_Url(TestEnvironment)
        headers = ModAFPO.getRuncaseEnvironment_Headers(TestEnvironment)

        #读取超时时间
        timeouttask = ModAFPO.getRuncaseEnvironment_Timeouttask(TestEnvironment)
        timeoutdelay = 0

        #启动mock
        StartResult = self.StartMock(MockData, ModAFPO, TestEnvironment)

        #驱动执行获得response
        PrintLog('debug', '[%s] 驱动执行:headers:%s TestData:%s', threading.currentThread().getName(), headers, TestData)
        DriverO = Interface_Driver.Interface_Http(url)
        DriverResult = DriverO.post(headers, TestData)     #执行用例
        PrintLog('debug', '[%s] 执行结果:DriverResult:%s', threading.currentThread().getName(), DriverResult)

        #结束mock
        self.EndMock(MockData, StartResult)

        #装载任务参数
        if DriverResult is False:
            return False
        taskargs = DriverResult
        return timeouttask, timeoutdelay, taskargs

    def RunCCSCase(self, sheet, testid, TestData, TestEnvironment, MockData):
        '''
        运行授信接口用例
        '''
        ModCCSO = ModCCS.ModCCS()
        dbinfo = ModCCSO.getRuncaseEnvironment_db(TestEnvironment)

        #读取超时时间
        timeouttask = ModCCSO.getRuncaseEnvironment_Timeouttask(TestEnvironment)
        timeoutdelay = 0

        #测试数据解析
        TestData, unique_id = ModCCSO.parseParamsForDriver(TestData)

        #启动mock
        StartResult = self.StartMock(MockData, ModCCSO, TestEnvironment)

        #驱动执行获得返回的唯一userid
        PrintLog('debug', '[%s] 驱动执行:TestData:%s\nunique_id: %s', threading.currentThread().getName(), TestData, unique_id)
        DriverO = Interface_Driver.Interface_DoData(dbinfo)
        DriverResult = DriverO.insert(TestData)    #执行用例
        PrintLog('debug', '[%s] 执行结果:DriverResult:%s', threading.currentThread().getName(), DriverResult)

        #结束mock
        self.EndMock(MockData, StartResult)

        #装载任务参数
        if DriverResult is False:
            return False
        taskargs = unique_id
        return timeouttask, timeoutdelay, taskargs

    def RunTestCase(self, sheet, testid):
        '''
        运行测试用例入口
        '''
        try:
            #获取执行用例所需的数据
            TestType = self.TestCaseO.get_TestType(sheet, testid)
            TestData = self.TestCaseO.get_TestData(sheet, testid)
            TestEnvironment = self.TestCaseO.get_TestEnvironment(sheet, testid)
            MockData = self.TestCaseO.get_MockData(sheet, testid)

            #执行用例
            if u'数据回流接口' == TestType:
                RunResult = self.RunUBASCase(sheet, testid, TestData, TestEnvironment)

            elif u'用户画像标签' == TestType:
                RunResult = self.RunUPSLabelCase(sheet, testid, TestData, TestEnvironment)

            elif u'用户画像接口' == TestType:
                RunResult = self.RunUPSCase(sheet, testid, TestData, TestEnvironment)

            elif u'反欺诈接口' == TestType:
                RunResult = self.RunAFPCase(sheet, testid, TestData, TestEnvironment, MockData)

            elif u'授信接口' == TestType:
                RunResult = self.RunCCSCase(sheet, testid, TestData, TestEnvironment, MockData)

            else:
                PrintLog('debug', 'TestType Value is Error')
                return False

            if RunResult is False:
                return False
            timeouttask, timeoutdelay, taskargs = RunResult

            #装载断言任务队列
            taskassert = (sheet, testid, timeouttask, timeoutdelay, taskargs)
            self.taskassert_queue.put(taskassert)
            return True

        except Exception as e:
            PrintLog('exception', e)
            return False
