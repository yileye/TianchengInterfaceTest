#coding=utf8
#######################################################
#filename:TestCase.py
#author:defias
#date:2015-11
#function: 测试用例类
#######################################################
from public import ExcelRW
import Config
import os


class MockDataXls(object):
    '''
    测试用例类
    '''
    datafilename = Config.ConfigIni.get_datafilename()
    if not os.path.isfile(datafilename):
        raise Exception, u'Don\'t find data file: %s' % datafilename

    xlseng = ExcelRW.XlsEngine(datafilename)
    mockdata_col = eval(Config.ConfigIni.get_mockdata_col())

    @classmethod
    def Id2rown(cls, ID):
        try:
            ID_col = cls.mockdata_col['ID']
            return cls.xlseng.readcol('HttpData', ID_col).index(float(ID))
        except:
            return False

    @classmethod
    def get_Key(cls, ID):
        '''
        获取Key
        '''
        Key_col = cls.mockdata_col['Key']
        Key_row = cls.Id2rown(ID)
        if Key_row is False:
            return False
        return cls.xlseng.readcell('HttpData', Key_row, Key_col)

    @classmethod
    def get_MockData(cls, ID):
        '''
        获取MockData
        '''
        MockData_col = cls.mockdata_col['MockData']
        MockData_row = cls.Id2rown(ID)
        if MockData_row is False:
            return False
        return cls.xlseng.readcell('HttpData', MockData_row, MockData_col)

    @classmethod
    def get_sheetAllID(cls):
        '''
        获取所有ID, 或指定sheet页中的所有testid
        '''
        ID_col = cls.mockdata_col['ID']
        alltestid = {}
        ID_allvalue = cls.xlseng.readcol('HttpData', ID_col)
        ID_allvalue = [x for x in ID_allvalue if type(x) is float] #过滤
        ID_allvalue = list(set(ID_allvalue))  #去重
        ID_allvalue = map(int,ID_allvalue)   #转为整数
        return ID_allvalue
