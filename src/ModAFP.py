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

    def parseExpForAssert(self, Expectation, TestData):
        '''
        解析期望结果数据
        '''
        try:
            if Expectation == '' or TestData == '':
                raise ValueError
            else:
                ExpectationDict = json.loads(Expectation)
                TestDataDict = json.loads(TestData)
            return ExpectationDict,TestDataDict
        except Exception as e:
            PrintLog('exception',e)
            return False



class ModAFP_Assert(object):
    '''
    AFP断言
    '''
    def __init__(self):
        pass

    def _checkdbdata(self, obj, unique, ExpectationDict, TestDataDict):
        '''
        检查数据库表中数据
        '''
        try:
            obj.connMy.select_db(obj.dbnameMy)   #选择数据库
            curMy = obj.connMy.cursor()

            ResultJsonExpDict = ExpectationDict.pop('ResultJson')
            for table in ExpectationDict.keys():
                fields = ExpectationDict[table].keys()
                values = ExpectationDict[table].values()

                query_where = (unique,)
                query_fields = 'resultJson,ReqJson,'
                for field in fields:
                    query_fields = query_fields + field + ','
                query_str = 'SELECT ' + query_fields[:-1] + ' FROM ' + table + ' WHERE UniqueID = %s'
                PrintLog('debug', '[%s] 执行SQL查询: query_str: %s %s', threading.currentThread().getName(), query_str, query_where)
                curMy.execute(query_str, query_where)
                obj.connMy.commit()
                result = curMy.fetchone()  #取查询结果第一条记录
                PrintLog('debug', '[%s] 数据库查询结果result: %s', threading.currentThread().getName(), result)

                #特殊加密字段
                if result == None:
                    return 'FAIL',u'数据库：%s 查询结果为空' % table

                result = list(result)
                resultJson = EncryptLib.getde_base64(result.pop(0))
                ReqJson = EncryptLib.getde_base64(result.pop(0))
                PrintLog('debug', '[%s] 数据库表中ReqJson字段值: %s', threading.currentThread().getName(), str(ReqJson).rstrip())
                PrintLog('debug', '[%s] 数据库表中resultJson字段值: %s', threading.currentThread().getName(), str(resultJson).rstrip())

                result = tuple(result)
                expvalues = tuple(values)
                PrintLog('debug', '[%s] 比较数据库表中数据与期望数据: result: %s\nexpvalues: %s', threading.currentThread().getName(), result, expvalues)
                assert result == expvalues, u'检查入库数据不正确'

                #检查请求数据
                ReqJsonDict = json_tools.loads(ReqJson)
                del ReqJsonDict['MsgBody']['UniqueID']   #去除UniqueID字段后进行比较
                PrintLog('debug', '[%s] 比较数据库表中ReqJson字段数据: TestDataDict: %s\nReqJsonDict: %s', threading.currentThread().getName(), TestDataDict, ReqJsonDict)
                assert json_tools.diff(TestDataDict, ReqJsonDict) == [], u'数据库表中ReqJson字段数据有误'

                #检查ResultJson
                resultJsonDict = json_tools.loads(resultJson)
                del resultJsonDict['Messge']
                del resultJsonDict['MsgBody']
                PrintLog('debug', '[%s] 比较数据库表中resultJson字段部分数据: ResultJsonExpDict: %s\nresultJsonDict: %s', threading.currentThread().getName(), ResultJsonExpDict, resultJsonDict)
                assert json_tools.diff(ResultJsonExpDict, resultJsonDict) == [], u'数据库表中ReqJson字段数据有误'
                return 'PASS',

        except AssertionError as e:
            return 'FAIL',unicode(e.args[0])
        except Exception as e:
            PrintLog('exception',e)
            return 'ERROR',unicode(e)


    def AFPAssert(self, obj, response, ExpectationDict, TestDataDict):
        '''
        AFP断言入口
        '''
        try:
            #检查响应
            response.encoding = response.apparent_encoding
            assert response.status_code == 200, u'HTTP响应码错误'

            responseContent =  unicode(response.content, "utf-8")
            responseContentDict = json.loads(responseContent)

            Expectation_HTTPResponse = ExpectationDict['HTTPResponse']
            Expectation_fieltlist = Expectation_HTTPResponse.keys()
            Expectation_valuelist = Expectation_HTTPResponse.values()

            PrintLog('debug','[%s] 比较响应数据与期望数据各字段: Expectation_HTTPResponse: %s responseContentDict: %s', threading.currentThread().getName(), Expectation_HTTPResponse, responseContentDict)
            for i in xrange(len(Expectation_fieltlist)):
                assert Expectation_valuelist[i] == responseContentDict[Expectation_fieltlist[i]], u'响应%s字段值不正确' % Expectation_fieltlist[i]

            unique = responseContentDict['unique']      #获取唯一标示号
            PrintLog('debug', '[%s] 唯一标示号unique: %s', threading.currentThread().getName(), unique)
            del ExpectationDict['HTTPResponse']
            return self._checkdbdata(obj, unique, ExpectationDict, TestDataDict)

        except AssertionError as e:
            return 'FAIL',unicode(e.args[0])
        except Exception as e:
            PrintLog('exception',e)
            return 'ERROR',unicode(e)



