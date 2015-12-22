#coding=utf8
#######################################################
#filename:ModUBAS.py
#author:defias
#date:2015-11
#function: UBAS相关
#######################################################
from Global import *
import threading
import Config
import MySQLdb

class ModUBAS(object):
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
        return timeoutdelay

    def getRuncaseEnvironment_Timeoutdelay(self, TestEnvironment):
        '''
        获取环境信息:timeoutdelay
        '''
        try:
            timeoutdelay = Config.ConfigIni.get_TestEnvironment_Info(TestEnvironment, 'timeoutdelay')
        except:
            return 0
        return timeoutdelay

    def parseExpForDriver(self, Expectation):
        '''
        解析期望结果数据
        '''
        try:
            if Expectation == '':
                raise ValueError
            else:
                ExpectationDict = json.loads(Expectation)
                del ExpectationDict['HTTPResponse']
            return ExpectationDict.keys()
        except Exception as e:
            PrintLog('exception',e)
            return False

    def parseExpForAssert(self, Expectation, Params):
        '''
        解析期望结果数据 变更表名
        '''
        try:
            OperateTimeTables = []   #需要增加操作时间后缀的表
            if Expectation == '':
                raise ValueError
            ExpectationDict = json.loads(Expectation)
            resultDict = {}

            for tablename in ExpectationDict.keys():
                if tablename in OperateTimeTables:
                    if Params == '':
                        raise ValueError
                    ParamsDict = json.loads(Params)
                    OperateTimedata = ParamsDict['operateTime'].split()[0]
                    pass
                    pass
                    tablenameT = tablename + OperateTimedata
                    resultDict[tablenameT] = ExpectationDict[tablename]
                else:
                    resultDict[tablename] = ExpectationDict[tablename]
            return resultDict
        except Exception as e:
            PrintLog('exception',e)
            return False


class ModUBAS_Assert(object):
    '''
    UBAS断言
    '''
    def __init__(self):
        pass

    def _checkdbdata(self, obj, tablemaxid, ExpectationDict):
        '''
        检查数据库表中数据
        '''
        try:
            obj.connMy.select_db(obj.dbnameMy)   #选择数据库
            curMy = obj.connMy.cursor()

            for table in ExpectationDict.keys():
                fields = ExpectationDict[table].keys()
                values = ExpectationDict[table].values()

                query_id = str(tablemaxid[table] + 1)
                query_fields = ''
                for field in fields:
                    query_fields = query_fields + field + ','
                query_fields = query_fields[:-1]
                query_str = 'SELECT ' + query_fields + ' FROM ' + table + ' WHERE id = ' + query_id
                PrintLog('debug', '[%s] 执行SQL查询: query_str: %s', threading.currentThread().getName(), query_str)
                curMy.execute(query_str)
                obj.connMy.commit()
                result = curMy.fetchone()

                expvalues = tuple(values)
                PrintLog('debug', '[%s] 比较数据库表中数据与期望数据: result: %s expvalues: %s', threading.currentThread().getName(), result, expvalues)
                assert result == expvalues, u'检查入库数据不正确'
                return 'PASS',

        except AssertionError as e:
            return 'FAIL',unicode(e.args[0])
        except Exception as e:
            PrintLog('exception',e)
            return 'ERROR',unicode(e)


    def UBASAssert(self, obj, response, tablemaxid, ExpectationDict):
        '''
        UBAS断言入口
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

            del ExpectationDict['HTTPResponse']
            return self._checkdbdata(obj, tablemaxid, ExpectationDict)

        except AssertionError as e:
            return 'FAIL',unicode(e.args[0])
        except Exception as e:
            PrintLog('exception',e)
            return 'ERROR',unicode(e)



