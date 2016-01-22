#coding=utf8
#######################################################
#filename: ModCCS.py
#author: defias
#date: 2015-12
#function: CCS相关
#######################################################
from Global import *
from public import EncryptLib
import threading
import Config
import uuid
import json
import json_tools
import re

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

    def getRuncaseEnvironment_HTTP(self, TestEnvironment):
        '''
        获取环境信息:HTTP信息
        '''
        HTTPhost = Config.ConfigIni.get_TestEnvironment_Info(TestEnvironment, 'HTTPhost')
        HTTPport = Config.ConfigIni.get_TestEnvironment_Info(TestEnvironment, 'HTTPport')
        HTTPinfo = (HTTPhost, int(HTTPport))
        return HTTPinfo

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

    def parseExpectationDict(self, ExpectationDict):
        '''
        提取加密字段数据
        '''
        prefix = r'^BASE64_'  #加密字段以BASE64_开头
        prelen = len(prefix)-1
        pattern = re.compile(prefix)
        ExpDict = dict()
        BASE64_ExpDict = dict()
        PrintLog('debug', '[%s] 提取加密字段数据from: ExpectationDict: %s', threading.currentThread().getName(), ExpectationDict)
        for table in ExpectationDict:
            TableValue = ExpectationDict[table]
            BASE64_ExpDict_Value = {key:TableValue[key] for key in TableValue if pattern.match(key)}
            BASE64_ExpDict_Value_outpre = {key[prelen:]:BASE64_ExpDict_Value[key] for key in BASE64_ExpDict_Value}
            BASE64_ExpDict[table] = BASE64_ExpDict_Value_outpre

            ExpDict_Value = {key:TableValue[key] for key in TableValue if key not in BASE64_ExpDict_Value}
            ExpDict[table] = ExpDict_Value
        return ExpDict, BASE64_ExpDict

    def checkExpDict(self, ExpDict, unique_id):
        '''
        检查明文字段
        '''
        for table in ExpDict:
            fields = ExpDict[table].keys()
            values = ExpDict[table].values()
            if not fields: continue
            PrintLog('debug', '[%s] 检查明文字段数据: 用例中读取的: fields: %s\nvalues: %s', threading.currentThread().getName(), fields, values)

            query_where = (unique_id,)
            query_fields = ''
            for field in fields:
                query_fields = query_fields + field + ', '
            query_str = 'SELECT ' + query_fields[:-2] + ' FROM ' + table + ' WHERE uid = %s'
            PrintLog('debug', '[%s] 执行SQL查询: query_str: %s %s', threading.currentThread().getName(), query_str, query_where)
            self.curMy.execute(query_str, query_where)
            self.obj.connMy.commit()
            result = self.curMy.fetchone()  #取查询结果第一条记录
            if result is None:
                raise  TableNoneError(u"%s is NONE" % table)

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
                            PrintLog('debug', '[%s] _检查明文字段数据: j_iresult[%s]: %s\nexpvalue[%s]: %s', threading.currentThread().getName(), key, j_iresult[key], key, expvalue[key])
                            assert json_tools.diff(json.dumps(j_iresult[key]), json.dumps(expvalue[key])) == [], u'_检查明文字段: %s字段中:%s字段数据与期望数据不一致' % (fields[i], key)
                        else:
                            PrintLog('debug', '[%s] 检查明文字段数据: j_iresult[%s]: %s\nexpvalue[%s]: %s', threading.currentThread().getName(), key, j_iresult[key], key, expvalue[key])
                            assert j_iresult[key] == expvalue[key], u'检查明文字段: %s字段中:%s字段数据与期望数据不一致' % (fields[i], key)
                else:
                    PrintLog('debug', '[%s] 检查明文%s字段数据: iresult: %s\nexpvalue: %s', threading.currentThread().getName(), fields[i], iresult, expvalue)
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
            query_str = 'SELECT ' + query_fields[:-2] + ' FROM ' + table + ' WHERE uid = %s'
            PrintLog('debug', '[%s] 执行SQL查询: query_str: %s %s', threading.currentThread().getName(), query_str, query_where)
            self.curMy.execute(query_str, query_where)
            self.obj.connMy.commit()
            result = self.curMy.fetchone()  #取查询结果第一条记录
            if result is None:
                raise  TableNoneError(u"%s is NONE" % table)

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
                            for kk in expvalue[key]:
                                assert kk in de_resultDict[key], u'检查BASE64加密字段: %s字段中:%s字段中无:%s字段' % (fields[i], key, kk)
                                if kk == 'fanyilist':
                                    PrintLog('debug', '[%s] _检查BASE64加密字段数据: de_resultDict[%s][%s]: %s\nexpvalue[%s][%s]: %s', threading.currentThread().getName(), key, kk, de_resultDict[key][kk], key, kk, expvalue[key][kk])
                                    self.check_fanyilist(de_resultDict[key][kk], expvalue[key][kk])
                                elif type(expvalue[key][kk]) is dict:
                                    PrintLog('debug', '[%s] _检查BASE64加密字段数据: de_resultDict[%s][%s]: %s\nexpvalue[%s][%s]: %s', threading.currentThread().getName(), key, kk, de_resultDict[key][kk], key, kk, expvalue[key][kk])
                                    assert json_tools.diff(json.dumps(de_resultDict[key][kk]), json.dumps(expvalue[key][kk])) == [], u'_检查BASE64加密字段: %s字段中:%s字段中:%s字段数据与期望数据不一致' % (fields[i], key, kk)
                                else:
                                    PrintLog('debug', '[%s] 检查BASE64加密字段数据: de_resultDict[%s][%s]: %s\nexpvalue[%s][%s]: %s', threading.currentThread().getName(), key, kk, de_resultDict[key][kk], key, kk, expvalue[key][kk])
                                    assert de_resultDict[key][kk] == expvalue[key][kk], u'检查BASE64加密字段: %s字段中:%s字段中:%s字段中数据与期望数据不一致' % (fields[i], key, kk)
                        else:
                            PrintLog('debug', '[%s] 检查BASE64加密字段数据: de_resultDict[%s]: %s\nexpvalue[%s]: %s', threading.currentThread().getName(), key, de_resultDict[key], key, expvalue[key])
                            assert de_resultDict[key] == expvalue[key], u'检查BASE64加密字段: %s字段中:%s字段数据与期望数据不一致' % (fields[i], key)
                else:
                    PrintLog('debug', '[%s] 检查BASE64加密%s字段数据: de_result: %s\nexpvalue: %s', threading.currentThread().getName(), fields[i], de_result, expvalue)
                    assert de_result == expvalue, u'检查BASE64加密字段: %s字段数据与期望数据不一致' % fields[i]

    def check_fanyilist(self, result, expvalue):
        '''
        检查fanyilist数据
        '''
        for i in xrange(len(expvalue)):
            assert 'mokuai' in result[i], u'检查fanyilist数据: 结果数据fanyilist中: 第%d项无mokuai字段' % i
            mokuai = result[i]['mokuai']
            assert 'weidu' in result[i], u'检查fanyilist数据: 结果数据fanyilist中: %s模块无weidu字段' % mokuai
            weidu = result[i]['weidu']

            assert 'mokuai' in expvalue[i], u'检查fanyilist数据: 期望数据fanyilist中: 第%d项无mokuai字段' % i
            expmokuai = expvalue[i]['mokuai']
            assert 'weidu' in expvalue[i], u'检查fanyilist数据: 期望数据fanyilist中: %s模块无weidu字段' % expmokuai
            expweidu = expvalue[i]['weidu']

            PrintLog('debug', '[%s] 检查fanyilist数据: fanyilist中:第%s项: mokuai: %s\nexpmokuai: %s', threading.currentThread().getName(), i, mokuai, expmokuai)
            assert mokuai == expmokuai, u'检查fanyilist数据: fanyilist中: 第%d项mokuai字段数据与期望数据不一致' % i

            for j in xrange(len(weidu)):
                assert type(weidu[j]) is dict, u'检查fanyilist数据: 结果数据fanyilist中: %s模块weidu中: 第%d项格式不正确' % (mokuai, j)
                assert type(expweidu[j]) is dict, u'检查fanyilist数据: 期望数据fanyilist中: %s模块weidu中: 第%d项格式不正确' % (mokuai, j)
                assert 'weiduming' in weidu[j], u'检查fanyilist数据: 结果数据fanyilist中: %s模块weidu中: 第%d项中无weiduming字段' % (mokuai, j)
                assert 'weiduming' in expweidu[j], u'检查fanyilist数据: 期望数据fanyilist中: %s模块weidu中: 第%d项中无weiduming字段' % (mokuai, j)

                weiduming = weidu[j]['weiduming']
                PrintLog('debug', '[%s] 检查fanyilist数据: fanyilist中: %s模块: %s维度: result: %s\nexpvalue: %s', threading.currentThread().getName(), mokuai, weiduming, weidu[j], expweidu[j])
                for k in expweidu[j]:
                    if type(expweidu[j][k]) is dict:
                        PrintLog('debug', '[%s] _检查fanyilist数据: fanyilist中: %s模块: %s维度: %s字段: %s\nexpvalue: %s', threading.currentThread().getName(), mokuai, weiduming, k, weidu[j][k], expweidu[j][k])
                        assert json_tools.diff(json.dumps(weidu[j][k]), json.dumps(expweidu[j][k])) == [], u'检查fanyilist数据: fanyilist中: mokuai: %s: weidu: %s %s字段数据与期望数据不一致' % (mokuai, weiduming, k)
                    else:
                        PrintLog('debug', '[%s] 检查fanyilist数据: fanyilist中: %s模块: %s维度: %s字段: %s\nexpvalue: %s', threading.currentThread().getName(), mokuai, weiduming, k, weidu[j][k], expweidu[j][k])
                        assert weidu[j][k] == expweidu[j][k], u'检查fanyilist数据: fanyilist中: mokuai: %s: weidu: %s \n%s字段数据与期望数据不一致' % (mokuai, weiduming, k)

    def CCSAssert(self, obj, ExpectationDict, unique_id):
        '''
        CCS断言入口
        '''
        try:
            self.obj = obj
            self.obj.connMy.select_db(self.obj.dbnameMy)   #选择数据库
            self.curMy = self.obj.connMy.cursor()
            ExpDict, BASE64_ExpDict = self.parseExpectationDict(ExpectationDict)
            PrintLog('debug', '[%s] 提取加密字段数据: ExpDict: %s\nBASE64_ExpDict: %s', threading.currentThread().getName(), ExpDict, BASE64_ExpDict)

            #检查明文数据
            self.checkExpDict(ExpDict, unique_id)

            #检查base64加密数据
            self.checkBASE64_ExpDict(BASE64_ExpDict, unique_id)
            return 'PASS',

        except TableNoneError as e:
            PrintLog('debug', '[%s] TableNoneError: TableName: %s', threading.currentThread().getName(), unicode(e))
            return 'NONE',unicode(e)
        except AssertionError as e:
            PrintLog('debug', '[%s] AssertionError: %s', threading.currentThread().getName(),unicode(e.args[0]))
            return 'FAIL',unicode(e.args[0])
        except Exception as e:
            PrintLog('exception',e)
            return 'ERROR',unicode(e)
