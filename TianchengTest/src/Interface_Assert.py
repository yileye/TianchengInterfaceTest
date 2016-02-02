#coding=utf8
#######################################################
#filename:Interface_Assert.py
#author:defias
#date:2015-11
#function: 天秤测试断言
#######################################################
from Global import *
import threading
import pymongo
import MySQLdb
import ModUPS
import ModUPSLabel
import ModUBAS
import ModAFP
import ModCCS

class Interface_Assert(object):
    '''
    断言类
    '''
    def __init__(self):
        pass

    def SetPublic_Mongodb(self, dbinfo):
        '''
        设置公共资源-数据库Mongodb
        '''
        host, port, username, passwd, dbname = dbinfo
        self.conn = pymongo.MongoClient(host=host,port=port)
        self.dbname = dbname
        PrintLog('debug', '[%s] connecting mongodb db: %s %s:%s %s/%s', threading.currentThread().getName(), dbname, host, port, username, passwd)

    def SetPublic_Mysql(self, dbinfo):
        '''
        设置公共资源-数据库Mysql
        '''
        host, port, username, passwd, dbname = dbinfo
        self.connMy = MySQLdb.connect(host=host,user=username,passwd=passwd,port=port,charset='utf8')  #连接数据库
        self.dbnameMy = dbname
        PrintLog('debug', '[%s] init connecting mysql db: %s %s:%s %s/%s', threading.currentThread().getName(), dbname, host, port, username, passwd)

    def __del__(self):
        '''
        释放公共资源
        '''
        if hasattr(self, 'cur'):
            pass
        if hasattr(self, 'conn'):
            pass
        if hasattr(self, 'curMy'):
            self.curMy.close()
        if hasattr(self, 'connMy'):
            self.connMy.close()
        PrintLog('debug', '[%s] Release  public resources', threading.currentThread().getName())

    def Assert_UPSLabel(self, expectation, useriduserid, *function):
        '''
        UPSLabel断言
        '''
        if function:
            PrintLog('debug', '[%s] 调用回调: 参数: %s', threading.currentThread().getName(), (expectation, useriduserid))
            cbresult = function[0](expectation, useriduserid)
            PrintLog('debug', '[%s] 回调结果:%s', threading.currentThread().getName(), cbresult)
            expectation = cbresult[0]
            useriduserid = cbresult[1]
        ModUPSLabel_AssertO = ModUPSLabel.ModUPSLabel_Assert()
        return ModUPSLabel_AssertO.UPSLabelAssert(self, expectation, useriduserid)


    def Assert_UPS(self, response, paramsDict, ExpectationDict):
        '''
        UPS接口断言
        '''
        ModUPS_AssertO = ModUPS.ModUPS_Assert()
        return ModUPS_AssertO.UPSAssert(self, response, paramsDict, ExpectationDict)


    def Assert_UBAS(self, response, tablemaxid, ExpectationDict):
        '''
        UBAS接口断言
        '''
        ModUBAS_AssertO = ModUBAS.ModUBAS_Assert()
        return ModUBAS_AssertO.UBASAssert(self, response, tablemaxid, ExpectationDict)


    def Assert_AFP(self, response, ExpectationDict):
        '''
        AFP接口断言
        '''
        ModAFP_AssertO = ModAFP.ModAFP_Assert()
        return ModAFP_AssertO.AFPAssert(self, response, ExpectationDict)

    def Assert_CCS(self, ExpectationDict, unique_id):
        '''
        CCS接口断言
        '''
        ModCCS_AssertO = ModCCS.ModCCS_Assert()
        return ModCCS_AssertO.CCSAssert(self,ExpectationDict, unique_id)
