#coding=utf8
#######################################################
#filename:ModCCS.py
#author:defias
#date:2015-12
#function: CCS相关 test
#######################################################
from Global import *
from public import EncryptLib
import threading
import Config
import uuid
import json
import json_tools

class ModCCS(object):
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

    def parseParamsForDriver(self, params):
        '''
        解析测试数据获取用例执行所需数据
        '''
        try:
            params_dict = json.loads(params)
            params_result = []
            tables = params_dict.keys()
            unique_id = str(uuid.uuid1())
            for table in tables:
                fields = params_dict[table].keys()
                values = params_dict[table].values()

                #json字段数据进行base64加密
                for i in xrange(len(fields)):
                    if fields[i] == 'json':
                        jsonvalue = json.dumps(values[i], ensure_ascii=False)
                        values[i] = EncryptLib.get_base64(jsonvalue.encode('utf8'))

                #添加唯一id字段
                fields.append('id')
                values.append(unique_id)
                params_result.append((table, fields, values))

            return params_result, unique_id

        except Exception as e:
            PrintLog('exception',e)
            return False

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



class ModCCS_Assert(object):
    '''
    CCS断言
    '''
    def __init__(self):
        pass

    def CCSAssert(self, obj, ExpectationDict, unique_id):
        '''
        CCS断言入口
        '''
        try:
            obj.connMy.select_db(obj.dbnameMy)   #选择数据库
            curMy = obj.connMy.cursor()

            sum_infoExpDict = ExpectationDict.pop('sum_info')
            for table in ExpectationDict.keys():
                fields = ExpectationDict[table].keys()
                values = ExpectationDict[table].values()

                query_where = (unique_id,)
                query_fields = 'sum_info, request, result,'
                for field in fields:
                    query_fields = query_fields + field + ','
                query_str = 'SELECT ' + query_fields[:-1] + ' FROM ' + table + ' WHERE uid = %s'
                PrintLog('debug', '[%s] 执行SQL查询: query_str: %s %s', threading.currentThread().getName(), query_str, query_where)
                curMy.execute(query_str, query_where)
                obj.connMy.commit()
                result = curMy.fetchone()  #取查询结果第一条记录
                PrintLog('debug', '[%s] 数据库查询结果result: %s', threading.currentThread().getName(), result)

                #特殊加密字段
                if result == None:
                    return 'FAIL',u'数据库：%s 查询结果为空' % table

                result = list(result)
                sum_info = EncryptLib.getde_base64(result.pop(0))
                request = EncryptLib.getde_base64(result.pop(0))
                resultresult = EncryptLib.getde_base64(result.pop(0))
                PrintLog('debug', '[%s] 数据库表中sum_info字段值: %s', threading.currentThread().getName(), str(sum_info).rstrip())
                PrintLog('debug', '[%s] 数据库表中request字段值: %s', threading.currentThread().getName(), str(request).rstrip())
                PrintLog('debug', '[%s] 数据库表中result字段值: %s', threading.currentThread().getName(), str(resultresult).rstrip())

                result = tuple(result)
                expvalues = tuple(values)
                PrintLog('debug', '[%s] 比较数据库表中数据与期望数据: result: %s\nexpvalues: %s', threading.currentThread().getName(), result, expvalues)
                assert result == expvalues, u'检查入库数据不正确'

                #检查sum_info中的各字段
                sum_infoDict = json_tools.loads(sum_info)
                for key in sum_infoExpDict:
                    assert key in sum_infoDict, u'sum_info中无期望的字段: {}'.format(key)

                sum_infoDict = {key:sum_infoDict[key] for key in sum_infoExpDict}

                PrintLog('debug', '[%s] 比较数据库表中sum_info字段部分数据: sum_infoExpDict: %s\nsum_infoDict: %s', threading.currentThread().getName(), sum_infoExpDict, sum_infoDict)
                assert json_tools.diff(sum_infoExpDict, sum_infoDict) == [], u'检查sum_info中数据有误'

            return 'PASS',

        except AssertionError as e:
            return 'FAIL',unicode(e.args[0])
        except Exception as e:
            PrintLog('exception',e)
            return 'ERROR',unicode(e)
