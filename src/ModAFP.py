#coding=utf8
#######################################################
#filename:ModAFP.py
#author:defias
#date:2015-12
#function: AFP相关
#######################################################
from Global import *
from public import EncryptLib
import threading
import Config
import MySQLdb
import json_tools
import re

class ModAFP(object):
    def __init__(self):
        pass

    def getRuncaseEnvironment_db(self, TestEnvironment):
        '''
        获取环境信息:数据库信息
        '''
        host = Config.ConfigIni.get_TestEnvironment_Info(TestEnvironment, 'host')
        port = Config.ConfigIni.get_TestEnvironment_Info(TestEnvironment, 'port')
        username = Config.ConfigIni.get_TestEnvironment_Info(TestEnvironment, 'username')
        password = Config.ConfigIni.get_TestEnvironment_Info(TestEnvironment, 'password')
        dbname = Config.ConfigIni.get_TestEnvironment_Info(TestEnvironment, 'dbname')
        dbinfo =  (host, int(port), username, password, dbname)
        return dbinfo

    def getRuncaseEnvironment_Url(self, TestEnvironment):
        '''
        获取环境信息:url
        '''
        url = Config.ConfigIni.get_TestEnvironment_Info(TestEnvironment, 'url')
        return url

    def getRuncaseEnvironment_Headers(self, TestEnvironment):
        '''
        获取环境信息:header
        '''
        headers = Config.ConfigIni.get_TestEnvironment_Info(TestEnvironment, 'headers')
        return eval(headers)

    def getRuncaseEnvironment_Timeouttask(self, TestEnvironment):
        '''
        获取环境信息: timeouttask
        '''
        try:
            timeouttask = Config.ConfigIni.get_TestEnvironment_Info(TestEnvironment, 'timeouttask')
        except:
            return 0
        return timeouttask

    def getRuncaseEnvironment_Timeoutdelay(self, TestEnvironment):
        '''
        获取环境信息:timeoutdelay
        '''
        try:
            timeoutdelay = Config.ConfigIni.get_TestEnvironment_Info(TestEnvironment, 'timeoutdelay')
        except:
            return 0
        return timeoutdelay

    def getRuncaseEnvironment_MQ(self, TestEnvironment):
        '''
        获取环境信息:MQ信息
        '''
        MQhost = Config.ConfigIni.get_TestEnvironment_Info(TestEnvironment, 'MQhost')
        MQport = Config.ConfigIni.get_TestEnvironment_Info(TestEnvironment, 'MQport')
        MQusername = Config.ConfigIni.get_TestEnvironment_Info(TestEnvironment, 'MQusername')
        MQpasswd = Config.ConfigIni.get_TestEnvironment_Info(TestEnvironment, 'MQpasswd')
        MQvhost = Config.ConfigIni.get_TestEnvironment_Info(TestEnvironment, 'MQvhost')
        MQinfo =  (MQhost, int(MQport), MQusername, MQpasswd, MQvhost)
        return MQinfo

    def getRuncaseEnvironment_TABLE(self, TestEnvironment):
        '''
        获取环境信息:TABLE信息
        '''
        TABLEhost = Config.ConfigIni.get_TestEnvironment_Info(TestEnvironment, 'TABLEhost')
        TABLEport = Config.ConfigIni.get_TestEnvironment_Info(TestEnvironment, 'TABLEport')
        TABLEusername = Config.ConfigIni.get_TestEnvironment_Info(TestEnvironment, 'TABLEusername')
        TABLEpassword = Config.ConfigIni.get_TestEnvironment_Info(TestEnvironment, 'TABLEpassword')
        TABLEdbname = Config.ConfigIni.get_TestEnvironment_Info(TestEnvironment, 'TABLEdbname')
        TABLEinfo =  (TABLEhost, int(TABLEport), TABLEusername, TABLEpassword, TABLEdbname)
        return TABLEinfo

    def parseExpForAssert(self, Expectation):
        '''
        解析期望结果数据
        '''
        try:
            if Expectation == '':
                raise ValueError
            else:
                ExpectationDict = json.loads(Expectation)
            return ExpectationDict
        except Exception as e:
            PrintLog('exception',e)
            return False

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


class ModAFP_Assert(object):
    '''
    AFP断言
    '''
    def __init__(self):
        pass

    def checkresponse(self, response, HTTPEXP):
        '''
        检查响应
        '''
        response.encoding = response.apparent_encoding
        assert response.status_code == 200, u'HTTP响应码错误: ErrorResponseCode: %s' % str(response.status_code)

        responseContent =  unicode(response.content, "utf-8")
        responseContentDict = json.loads(responseContent)

        #获取唯一标示号
        if 'unique' not in responseContentDict:
            raise AssertionError, u'检查响应: 响应responseContentDict中无唯一标示号unique'
        unique_id = responseContentDict['unique']
        PrintLog('debug','[%s] 检查响应: unique_id: %s\nHTTPEXP: %s\nresponseContentDict: %s', threading.currentThread().getName(), unique_id, HTTPEXP, responseContentDict)

        if HTTPEXP is not None:
            assert type(HTTPEXP) is dict , u'HTTPEXP数据格式错误：type of HTTPEXP is %s' % type(HTTPEXP)
            for key in HTTPEXP:
                assert key in responseContentDict, u'检查响应: 响应responseContentDict中无%s字段' % key
                assert responseContentDict[key] == HTTPEXP[key], u'检查响应: 响应responseContentDict中%s字段值与期望数据不一致' % key
        return unique_id

    def checkExpDict(self, ExpDict, unique_id):
        '''
        检查明文字段
        '''
        for table in ExpDict:
            fields = ExpDict[table].keys()
            values = ExpDict[table].values()
            if not fields: continue
            PrintLog('debug', '[%s] 检查明文字段数据: 用例中读取的fields: %s\nvalues: %s', threading.currentThread().getName(), fields, values)

            query_where = (unique_id,)
            query_fields = ''
            for field in fields:
                query_fields = query_fields + field + ', '
            query_str = 'SELECT ' + query_fields[:-2] + ' FROM ' + table + ' WHERE UniqueID = %s'
            PrintLog('debug', '[%s] 执行SQL查询: query_str: %s %s', threading.currentThread().getName(), query_str, query_where)
            self.curMy.execute(query_str, query_where)
            self.obj.connMy.commit()
            result = self.curMy.fetchone()  #取查询结果第一条记录
            if result is None:
                raise AssertionError, u'%s表中查询结果为空' % table

            expvalues = tuple(values)
            PrintLog('debug', '[%s] 检查明文字段数据: result: %s\nexpvalues: %s', threading.currentThread().getName(), result, expvalues)
            for i in range(len(fields)):
                expvalue = expvalues[i]
                iresult = result[i]
                if type(expvalue) is dict:
                    try:
                        j_iresult = json_tools.loads(iresult)
                    except:
                        raise AssertionError, u'_检查明文字段: %s字段数据与期望数据不一致' % fields[i]
                    for key in expvalue:
                        assert key in j_iresult, u'检查明文字段: %s字段中无:%s字段' % (fields[i], key)
                        if type(expvalue[key]) is dict:
                            PrintLog('debug', '[%s] _检查明文字段数据: j_iresult[%s]: %s  expvalue[%s]: %s', threading.currentThread().getName(), key, j_iresult[key], key, expvalue[key])
                            assert json_tools.diff(json.dumps(j_iresult[key]), json.dumps(expvalue[key])) == [], u'_检查明文字段: %s字段中:%s字段数据与期望数据不一致' % (fields[i], key)
                        else:
                            PrintLog('debug', '[%s] 检查明文字段数据: j_iresult[%s]: %s  expvalue[%s]: %s', threading.currentThread().getName(), key, j_iresult[key], key, expvalue[key])
                            assert j_iresult[key] == expvalue[key], u'检查明文字段: %s字段中:%s字段数据与期望数据不一致' % (fields[i], key)
                else:
                    PrintLog('debug', '[%s] 检查明文字段%s数据: iresult: %s  expvalue: %s', threading.currentThread().getName(), fields[i], iresult, expvalue)
                    assert iresult == expvalue, u'检查明文字段数据: %s字段数据与期望数据不一致' % fields[i]

    def checkBASE64_ExpDict(self, BASE64_ExpDict, unique_id):
        '''
        检查BASE64加密字段
        '''
        for table in BASE64_ExpDict:
            fields = BASE64_ExpDict[table].keys()
            values = BASE64_ExpDict[table].values()
            if not fields: continue
            PrintLog('debug', '[%s] 检查BASE64加密字段数据: 用例中读取的fields: %s\nvalues: %s', threading.currentThread().getName(), fields, values)

            query_where = (unique_id,)
            query_fields = ''
            for field in fields:
                query_fields = query_fields + field + ', '
            query_str = 'SELECT ' + query_fields[:-2] + ' FROM ' + table + ' WHERE UniqueID = %s'
            PrintLog('debug', '[%s] 执行SQL查询: query_str: %s %s', threading.currentThread().getName(), query_str, query_where)
            self.curMy.execute(query_str, query_where)
            self.obj.connMy.commit()
            result = self.curMy.fetchone()  #取查询结果第一条记录
            if result is None:
                raise AssertionError, u'%s表中查询结果为空' % table

            expvalues = tuple(values)
            for i in range(len(fields)):
                expvalue = expvalues[i]
                de_result = EncryptLib.getde_base64(result[i])
                PrintLog('debug', '[%s] 检查BASE64加密字段数据: de_result: %s\nexpvalue: %s', threading.currentThread().getName(), de_result, expvalue)
                if type(expvalue) is dict:
                    try:
                        de_resultDict = json_tools.loads(de_result)
                        PrintLog('debug', '[%s] 检查BASE64加密字段数据: de_resultDict: %s', threading.currentThread().getName(), de_resultDict)
                    except:
                        raise AssertionError, u'_检查BASE64加密字段: %s字段数据与期望数据不一致' % fields[i]

                    for key in expvalue:
                        assert key in de_resultDict, u'检查BASE64加密字段: %s字段中无:%s字段' % (fields[i], key)
                        if type(expvalue[key]) is dict:
                            PrintLog('debug', '[%s] _检查BASE64加密字段数据: de_resultDict[%s]: %s  expvalue[%s]: %s', threading.currentThread().getName(), key, de_resultDict[key], key, expvalue[key])
                            assert json_tools.diff(json.dumps(de_resultDict[key]), json.dumps(expvalue[key])) == [], u'_检查BASE64加密字段: %s字段中:%s字段数据与期望数据不一致' % (fields[i], key)
                        else:
                            PrintLog('debug', '[%s] 检查BASE64加密字段数据: de_resultDict[%s]: %s  expvalue[%s]: %s', threading.currentThread().getName(), key, de_resultDict[key], key, expvalue[key])
                            assert de_resultDict[key] == expvalue[key], u'检查BASE64加密字段: %s字段中:%s字段数据与期望数据不一致' % (fields[i], key)
                else:
                    PrintLog('debug', '[%s] 检查BASE64加密字段%s数据: de_result: %s  expvalue: %s', threading.currentThread().getName(), fields[i], de_result, expvalue)
                    assert de_result == expvalue, u'检查BASE64加密字段: %s字段数据与期望数据不一致' % fields[i]

    def parseExpectationDict(self, ExpectationDict):
        '''
        提取加密字段和响应数据
        '''
        PrintLog('debug', '[%s] 提取加密字段和响应数据from: ExpectationDict: %s', threading.currentThread().getName(), ExpectationDict)
        HTTPEXP = None
        #提取响应数据
        if 'HTTPEXP' in ExpectationDict:
            HTTPEXP = ExpectationDict.pop('HTTPEXP')

        #提取加密字段数据
        prefix = r'^BASE64_'  #加密字段以BASE64_开头
        prelen = len(prefix)-1
        pattern = re.compile(prefix)
        ExpDict = dict()
        BASE64_ExpDict = dict()

        for table in ExpectationDict:
            TableValue = ExpectationDict[table]
            BASE64_ExpDict_Value = {key:TableValue[key] for key in TableValue if pattern.match(key)}
            BASE64_ExpDict_Value_outpre = {key[prelen:]:BASE64_ExpDict_Value[key] for key in BASE64_ExpDict_Value}
            BASE64_ExpDict[table] = BASE64_ExpDict_Value_outpre

            ExpDict_Value = {key:TableValue[key] for key in TableValue if key not in BASE64_ExpDict_Value}
            ExpDict[table] = ExpDict_Value
        return HTTPEXP, ExpDict, BASE64_ExpDict

    def AFPAssert(self, obj, response, ExpectationDict):
        '''
        AFP断言入口
        '''
        try:
            self.obj = obj
            self.obj.connMy.select_db(self.obj.dbnameMy)   #选择数据库
            self.curMy = self.obj.connMy.cursor()
            HTTPEXP, ExpDict, BASE64_ExpDict = self.parseExpectationDict(ExpectationDict)
            PrintLog('debug', '[%s] 提取加密字段数据: HTTPEXP: %s\nExpDict: %s\nBASE64_ExpDict: %s', threading.currentThread().getName(), HTTPEXP, ExpDict, BASE64_ExpDict)

            #检查响应
            unique_id = self.checkresponse(response, HTTPEXP)

            #检查明文数据
            self.checkExpDict(ExpDict, unique_id)

            #检查base64加密数据
            self.checkBASE64_ExpDict(BASE64_ExpDict, unique_id)
            return 'PASS',

        except AssertionError as e:
            return 'FAIL',unicode(e.args[0])
        except Exception as e:
            PrintLog('exception',e)
            return 'ERROR',unicode(e)
