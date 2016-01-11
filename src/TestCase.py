#coding=utf8
#######################################################
#filename:TestCase.py
#author:defias
#date:2015-11
#function: 测试用例类
#######################################################
from public import ExcelRW
import Config


class TestCaseXls(object):
    '''
    测试用例类
    '''
    case_path = '.\\TestCase.xlsx'
    xlseng = ExcelRW.XlsEngine(case_path)
    testcase_col = eval(Config.ConfigIni.get_testcase_col())

    @classmethod
    def get_CaseSheets(cls):
        '''
        获取用例文件所有sheet
        '''
        return cls.xlseng.getsheets()

    @classmethod
    def Testid2rown(cls, sheet, testid):
        try:
            testid_col = cls.testcase_col['TestId']
            return cls.xlseng.readcol(sheet, testid_col).index(float(testid))
        except:
            return False

    @classmethod
    def get_TestCaseName(cls, sheet, testid):
        '''
        获取TestCaseName
        '''
        TestCaseName_col = cls.testcase_col['TestCaseName']
        TestCaseName_row = cls.Testid2rown(sheet, testid)
        if TestCaseName_row is False:
            return False
        return cls.xlseng.readcell(sheet, TestCaseName_row, TestCaseName_col)

    @classmethod
    def get_TestCaseId(cls, sheet, testid):
        '''
        获取TestCaseId
        '''
        TestCaseId_col = cls.testcase_col['TestCaseId']
        TestCaseId_row = cls.Testid2rown(sheet, testid)
        if TestCaseId_row is False:
            return False
        return cls.xlseng.readcell(sheet, TestCaseId_row, TestCaseId_col)

    @classmethod
    def get_TestItem(cls, sheet, testid):
        '''
        获取TestItem
        '''
        TestItem_col = cls.testcase_col['TestItem']
        TestItem_row = cls.Testid2rown(sheet, testid)
        if TestItem_row is False:
            return False
        return cls.xlseng.readcell(sheet, TestItem_row, TestItem_col)

    @classmethod
    def get_TestType(cls, sheet, testid):
        '''
        获取TestType
        '''
        TestType_col = cls.testcase_col['TestType']
        TestType_row = cls.Testid2rown(sheet, testid)
        if TestType_row is False:
            return False
        return cls.xlseng.readcell(sheet, TestType_row, TestType_col)

    @classmethod
    def get_TestEnvironment(cls, sheet, testid):
        '''
        获取TestEnvironment
        '''
        TestEnvironment_col = cls.testcase_col['TestEnvironment']
        TestEnvironment_row = cls.Testid2rown(sheet, testid)
        if TestEnvironment_row is False:
            return False
        return cls.xlseng.readcell(sheet, TestEnvironment_row, TestEnvironment_col)

    @classmethod
    def get_TestData(cls, sheet, testid):
        '''
        获取TestData
        '''
        TestData_col = cls.testcase_col['TestData']
        TestData_row = cls.Testid2rown(sheet, testid)
        if TestData_row is False:
            return False
        return cls.xlseng.readcell(sheet, TestData_row, TestData_col)

    @classmethod
    def get_Expectation(cls, sheet, testid):
        '''
        获取Expectation
        '''
        Expectation_col = cls.testcase_col['Expectation']
        Expectation_row = cls.Testid2rown(sheet, testid)
        if Expectation_row is False:
            return False
        return cls.xlseng.readcell(sheet, Expectation_row, Expectation_col)

    @classmethod
    def get_MockData(cls, sheet, testid):
        '''
        获取MockData
        '''
        MockData_col = cls.testcase_col['MockData']
        MockData_row = cls.Testid2rown(sheet, testid)
        if MockData_row is False:
            return False
        return cls.xlseng.readcell(sheet, MockData_row, MockData_col)

    @classmethod
    def get_Alltestid(cls, *sheet):
        '''
        获取所有testid, 或指定sheet页中的所有testid
        '''
        testid_col = cls.testcase_col['TestId']
        if sheet:
            if type(sheet[0]) is list:
                sheetlist = sheet[0]
            else:
                sheetlist = [sheet[0]]
        else:
            sheetlist = cls.xlseng.getsheets()
        alltestid = {}
        for sheet in sheetlist:
            testid_allvalue = cls.xlseng.readcol(sheet, testid_col)
            testid_allvalue = [x for x in testid_allvalue if type(x) is float] #过滤
            testid_allvalue = list(set(testid_allvalue))  #去重
            testid_allvalue = map(int,testid_allvalue) #转为整数
            alltestid[sheet] = testid_allvalue
        return alltestid
