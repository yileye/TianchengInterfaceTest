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
import TestCase


class ModMock(object):
    def __init__(self):
        pass

    def getRuncaseEnvironment_MQ(self):
        '''
        获取环境信息:MQ信息
        '''
        MQhost = Config.ConfigIni.get_TestEnvironment_Info('MOCK', 'MQhost')
        MQport = Config.ConfigIni.get_TestEnvironment_Info('MOCK', 'MQport')
        MQusername = Config.ConfigIni.get_TestEnvironment_Info('MOCK', 'MQusername')
        MQpasswd = Config.ConfigIni.get_TestEnvironment_Info('MOCK', 'MQpasswd')
        MQvhost = Config.ConfigIni.get_TestEnvironment_Info('MOCK', 'MQvhost')
        MQinfo =  (MQhost, int(MQport), MQusername, MQpasswd, MQvhost)
        return MQinfo

    def getRuncaseEnvironment_HTTP(self):
        '''
        获取环境信息:HTTP信息
        '''
        HTTPhost = Config.ConfigIni.get_TestEnvironment_Info('MOCK', 'HTTPhost')
        HTTPport = Config.ConfigIni.get_TestEnvironment_Info('MOCK', 'HTTPport')
        HTTPinfo = (HTTPhost, int(HTTPport))
        return HTTPinfo

    def getRuncaseEnvironment_TABLE(self):
        '''
        获取环境信息:TABLE信息
        '''
        TABLEhost = Config.ConfigIni.get_TestEnvironment_Info('MOCK', 'TABLEhost')
        TABLEport = Config.ConfigIni.get_TestEnvironment_Info('MOCK', 'TABLEport')
        TABLEusername = Config.ConfigIni.get_TestEnvironment_Info('MOCK', 'TABLEusername')
        TABLEpassword = Config.ConfigIni.get_TestEnvironment_Info('MOCK', 'TABLEpassword')
        TABLEdbname = Config.ConfigIni.get_TestEnvironment_Info('MOCK', 'TABLEdbname')
        TABLEinfo =  (TABLEhost, int(TABLEport), TABLEusername, TABLEpassword, TABLEdbname)
        return TABLEinfo

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

            HTTPMockDate = None
            MQMockData = None
            TABLEData = None
            if 'HTTPMOCK' in MockDataDict:
                HTTPMockDate = MockDataDict['HTTPMOCK']
            if 'MQMOCK' in MockDataDict:
                MQMockData = MockDataDict['MQMOCK']
            if 'TABLE' in MockDataDict:
                TABLEData = MockDataDict['TABLE']
            return HTTPMockDate,MQMockData,TABLEData
        except Exception as e:
            PrintLog('exception',e)
            return False

    def getSheetId_from_identity_card(self, identity_card):
        '''
        通过identity_card获取sheetid
        '''
        sheetid_identity_card = eval(memdata.getvalue().split('+++')[2])
        sheetid_identity_cardi = filter(lambda x: x[1]==identity_card,sheetid_identity_card.items())
        sheetids =  [x[0] for x in sheetid_identity_cardi]
        return sheetids[0]

    def getSheetId_from_UserMobile(self, UserMobile):
        '''
        通过identity_card获取sheetid
        '''
        sheetid_UserMobile = eval(memdata.getvalue().split('+++')[3])
        sheetid_UserMobilei = filter(lambda x: x[1]==UserMobile,sheetid_UserMobile.items())
        sheetids =  [x[0] for x in sheetid_UserMobilei]
        return sheetids[0]

    def SheetId_identity_card(self, TestIds):
        '''
        从待执行用例TestIds中查找identity_card
        '''
        sheetid_identity_card = {}
        for sheet in TestIds:
            for testid in TestIds[sheet]:
                try:
                    TestData = TestCase.TestCaseXls.get_TestData(sheet, testid)
                    if TestData is not False and TestData != '':
                        TestDataDict = json.loads(TestData)
                        if type(TestDataDict) is list:
                            TestDataDict = TestDataDict[1]
                        if "MsgBody" in TestDataDict:
                            identity_card = TestDataDict['MsgBody']['identity_card']
                            sheetid_identity_card[(sheet, testid)] = identity_card
                            continue
                        if 'identity_card' in TestDataDict:
                            identity_card = TestDataDict['identity_card']
                            sheetid_identity_card[(sheet, testid)] = identity_card
                            continue
                        if 'IdentitytCard' in TestDataDict.values()[0]:
                            identity_card = TestDataDict.values()[0]['IdentitytCard']
                            sheetid_identity_card[(sheet, testid)] = identity_card
                            continue
                        if 'json' in TestDataDict.values()[0]:
                            identity_card = TestDataDict.values()[0]['json']['UserBasicInfo']['IdentityCard']
                            sheetid_identity_card[(sheet, testid)] = identity_card
                            continue
                        continue
                    continue
                except Exception as e:
                    continue
        #查重
        if len(sheetid_identity_card.values()) != len(set(sheetid_identity_card.values())):
            PrintLog('debug', 'sheetid_identity_card中存在重复数据: %s', sheetid_identity_card)
            return False
        return sheetid_identity_card

    def SheetId_UserMobile(self, TestIds):
        '''
        从待执行用例TestIds中查找UserMobile
        '''
        sheetid_UserMobile = {}
        for sheet in TestIds:
            for testid in TestIds[sheet]:
                try:
                    TestData = TestCase.TestCaseXls.get_TestData(sheet, testid)
                    if TestData is not False and TestData != '':
                        TestDataDict = json.loads(TestData)
                        if 'Phone' in TestDataDict.values()[0]:
                            UserMobile = TestDataDict.values()[0]['Phone']
                            sheetid_UserMobile[(sheet, testid)] = UserMobile
                            continue
                        if 'json' in TestDataDict.values()[0]:
                            UserMobile = TestDataDict.values()[0]['json']['UserBasicInfo']['TelNo']
                            sheetid_UserMobile[(sheet, testid)] = UserMobile
                            continue
                        continue
                    continue
                except Exception as e:
                    continue
        #查重
        if len(sheetid_UserMobile.values()) != len(set(sheetid_UserMobile.values())):
            PrintLog('debug', 'sheetid_UserMobile中存在重复数据: %s', sheetid_UserMobile)
            return False
        return sheetid_UserMobile
