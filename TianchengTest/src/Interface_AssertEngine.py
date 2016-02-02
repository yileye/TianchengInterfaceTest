#coding=utf8
#######################################################
#filename:Interface_AssertEngine.py
#author:defias
#date:2015-7
#function:
#######################################################
from Global import *
import threading
import TestCase
import Interface_Assert
import ModUPS
import ModUPSLabel
import ModUBAS
import ModAFP
import ModCCS

class Interface_AssertEngine():
    '''
    断言测试结果
    '''
    def __init__(self):
        self.TestCaseO = TestCase.TestCaseXls

    def AssertUBASCase(self, sheet, testid, taskargs, Expectation, TestEnvironment):
        '''
        断言数据回流接口用例执行结果
        '''
        ModUBASO = ModUBAS.ModUBAS()
        dbinfo = ModUBASO.getRuncaseEnvironment_db(TestEnvironment)
        #读取任务参数中的数据
        response,tablemaxid = taskargs

        #获取断言数据所需条件where
        TestData = self.TestCaseO.get_TestData(sheet, testid)
        ExpectationDict = ModUBASO.parseExpForAssert(Expectation, TestData)

        #断言执行
        PrintLog('debug', '[%s] 驱动断言:response:%s tablemaxid:%s ExpectationDict:%s', threading.currentThread().getName(), response, tablemaxid, ExpectationDict)
        AssertO = Interface_Assert.Interface_Assert()
        AssertO.SetPublic_Mysql(dbinfo)
        AssertResult = AssertO.Assert_UBAS(response, tablemaxid, ExpectationDict)
        return AssertResult

    def AssertUPSCase(self, sheet, testid, taskargs, Expectation, TestEnvironment):
        '''
        断言用户画像接口用例执行结果
        '''
        ModUPSO = ModUPS.ModUPS()
        TestEnvironmentDB = TestEnvironment + '_Label'  #使用用户画像标签的数据信息
        dbinfo_Userdb = ModUPSO.getRuncaseEnvironment_Userdb(TestEnvironmentDB)
        dbinfo_Labeldb = ModUPSO.getRuncaseEnvironment_Labeldb(TestEnvironmentDB)
        response = taskargs

        #获取断言数据所需条件where
        TestData = self.TestCaseO.get_TestData(sheet, testid)
        paramsDict = ModUPSO.parseParamsForAssert(TestData)
        ExpectationDict = ModUPSO.parseExpForAssert(Expectation)

        #断言执行
        PrintLog('debug', '[%s] 驱动断言:response:%s paramsDict:%s ExpectationDict:%s', threading.currentThread().getName(), response, paramsDict, ExpectationDict)
        AssertO = Interface_Assert.Interface_Assert()
        AssertO.SetPublic_Mongodb(dbinfo_Labeldb)
        AssertO.SetPublic_Mysql(dbinfo_Userdb)
        AssertResult = AssertO.Assert_UPS(response, paramsDict, ExpectationDict)
        return AssertResult

    def AssertUPSLabelCase(self, sheet, testid, taskargs, Expectation, TestEnvironment):
        '''
        断言用户画像标签用例执行结果
        '''
        ModUPSLabelO = ModUPSLabel.ModUPSLabel()
        dbinfo = ModUPSLabelO.getRuncaseEnvironment_Labeldb(TestEnvironment)
        function = ModUPSLabelO.AssertCbFunction
        userid = taskargs
        PrintLog('debug', '[%s] 驱动断言:Expectation:%s CbFunction:%s', threading.currentThread().getName(), Expectation, function.__name__)
        AssertO = Interface_Assert.Interface_Assert()
        AssertO.SetPublic_Mongodb(dbinfo)
        AssertResult = AssertO.Assert_UPSLabel(Expectation, userid, function)
        return AssertResult

    def AssertAFPCase(self, sheet, testid, taskargs, Expectation, TestEnvironment):
        '''
        断言反欺诈接口用例执行结果
        '''
        ModAFPO = ModAFP.ModAFP()
        dbinfo = ModAFPO.getRuncaseEnvironment_db(TestEnvironment)

        #读取任务参数中的数据
        response = taskargs

        #获取断言数据
        ExpectationDict = ModAFPO.parseExpForAssert(Expectation)

        #断言执行
        PrintLog('debug', '[%s] 驱动断言:response:%s ExpectationDict:%s', threading.currentThread().getName(), response, ExpectationDict)
        AssertO = Interface_Assert.Interface_Assert()
        AssertO.SetPublic_Mysql(dbinfo)
        AssertResult = AssertO.Assert_AFP(response, ExpectationDict)
        return AssertResult

    def AssertCCSCase(self, sheet, testid, taskargs, Expectation, TestEnvironment):
        '''
        断言授信接口用例执行结果
        '''
        ModCCSO = ModCCS.ModCCS()
        dbinfo = ModCCSO.getRuncaseEnvironment_db(TestEnvironment)

        #读取任务参数中的数据
        unique_id = taskargs

        #获取断言数据
        ExpectationDict = ModCCSO.parseExpForAssert(Expectation)


        #断言执行
        PrintLog('debug', '[%s] 驱动断言:ExpectationDict:%s unique_id: %s', threading.currentThread().getName(), ExpectationDict, unique_id)
        AssertO = Interface_Assert.Interface_Assert()
        AssertO.SetPublic_Mysql(dbinfo)
        AssertResult = AssertO.Assert_CCS(ExpectationDict, unique_id)
        return AssertResult


    def AssertTestCase(self, sheet, testid, taskargs):
        '''
        断言测试用例执行结果入口
        '''
        try:
            #获取断言用例所需数据
            TestType = self.TestCaseO.get_TestType(sheet, testid)
            TestEnvironment = self.TestCaseO.get_TestEnvironment(sheet, testid)
            Expectation = self.TestCaseO.get_Expectation(sheet, testid)

            #断言用例
            if u'数据回流接口' == TestType:
                AssertResult = self.AssertUBASCase(sheet, testid, taskargs, Expectation, TestEnvironment)

            elif u'用户画像标签' == TestType:
                AssertResult = self.AssertUPSLabelCase(sheet, testid, taskargs, Expectation, TestEnvironment)

            elif u'用户画像接口' == TestType:
                AssertResult = self.AssertUPSCase(sheet, testid, taskargs, Expectation, TestEnvironment)

            elif u'反欺诈接口' == TestType:
                AssertResult = self.AssertAFPCase(sheet, testid, taskargs, Expectation, TestEnvironment)

            elif u'授信接口' == TestType:
                AssertResult = self.AssertCCSCase(sheet, testid, taskargs, Expectation, TestEnvironment)

            else:
                AssertResult = 'ERROR',u'TestType ValueError'
            return AssertResult

        except Exception as e:
                PrintLog('exception', e)
                return 'ERROR',unicode(e)

