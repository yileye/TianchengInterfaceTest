#coding=utf8
#######################################################
#filename:ModUPS.py
#author:defias
#date:2015-11
#function: UPSLabel相关
#######################################################
from Global import *
import threading
import Config
import json

class ModUPS(object):
    def __init__(self):
        pass

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

    def getRuncaseEnvironment_Userdb(self, TestEnvironment):
        '''
        获取环境信息:用户数据库信息
        '''
        host = Config.ConfigIni.get_TestEnvironment_Info(TestEnvironment, 'userdb_host')
        port = Config.ConfigIni.get_TestEnvironment_Info(TestEnvironment, 'userdb_port')
        username = Config.ConfigIni.get_TestEnvironment_Info(TestEnvironment, 'userdb_username')
        password = Config.ConfigIni.get_TestEnvironment_Info(TestEnvironment, 'userdb_password')
        name = Config.ConfigIni.get_TestEnvironment_Info(TestEnvironment, 'userdb_name')
        dbinfo =  (host, int(port), username, password, name)
        return dbinfo

    def getRuncaseEnvironment_Labeldb(self, TestEnvironment):
        '''
        获取环境信息:标签数据库信息
        '''
        labeldb_host = Config.ConfigIni.get_TestEnvironment_Info(TestEnvironment, 'labeldb_host')
        labeldb_port = Config.ConfigIni.get_TestEnvironment_Info(TestEnvironment, 'labeldb_port')
        labeldb_username = Config.ConfigIni.get_TestEnvironment_Info(TestEnvironment, 'labeldb_username')
        labeldb_password = Config.ConfigIni.get_TestEnvironment_Info(TestEnvironment, 'labeldb_password')
        labeldb_name = Config.ConfigIni.get_TestEnvironment_Info(TestEnvironment, 'labeldb_name')
        labeldbinfo =  (labeldb_host, int(labeldb_port), labeldb_username, labeldb_password, labeldb_name)
        return labeldbinfo

    def parseParamsForAssert(self,params):
        '''
        解析测试数据获取断言所需数据
        '''
        paramsDict = json.loads(params)
        return paramsDict

    def parseExpForAssert(self, Expectation):
        '''
        解析期望结果获取断言所需数据
        '''
        if Expectation == '':
            ExpectationDict = ''
        else:
            ExpectationDict = json.loads(Expectation)
        return ExpectationDict





class ModUPS_Assert(object):
    '''
    UPS断言
    '''
    def __init__(self):
        pass

    def _labels2id(self, obj, labels_name):
        '''
        将标签名列表转为标签id列表
        '''
        dbname = 'ups'   #标签名转为标签id的数据库名称
        obj.connMy.select_db(dbname)   #选择数据库
        curMy = obj.connMy.cursor()
        labels_name = tuple(labels_name)
        labels_count = len(labels_name)
        where = "("
        for i in xrange(labels_count):
            where = where + "%s,"
        where = where[:-1] + ")"
        selectStr = "SELECT label_id FROM ups_label WHERE label_name in " + where
        curMy.execute(selectStr, labels_name)
        result = curMy.fetchmany(labels_count)
        if len(result) == 0:
            result = []
        else:
            result = map(int, [x[0] for x in result])
        return result

    def _getlabels_mobile_phone(self, obj, mobile_phone):
        '''
        通过手机号获得标签id列表
        '''
        obj.connMy.select_db(obj.dbnameMy)   #选择数据库
        curMy = obj.connMy.cursor()
        curMy.execute("SELECT  UserID  FROM userbasicinfo WHERE MobilePhone = %s", (mobile_phone,))
        result = curMy.fetchone()
        PrintLog('debug','[%s] 通过手机号获得userid: result: %s', threading.currentThread().getName(), result)
        if result is None:
            return []
        userid = result[0]

        db = obj.conn[obj.dbname]      #选择mongodb数据库
        account = db['userlabelquery']
        query_where = {}
        query_where['userId'] = userid
        result = account.find_one(query_where)
        PrintLog('debug', '[%s] 通过手机号获得标签id: result: %s', threading.currentThread().getName(), result)
        if result is not  None:
            result = map(int,result['labelIds'])
        else:
            result = []
        return result


    def _getlabels_id_card(self, obj, id_card):
        '''
        通过身份证号获得标签id列表
        '''
        if type(id_card) in [long, int]:
            id_card = str(id_card)
        #查询userid
        obj.connMy.select_db(obj.dbnameMy)   #选择数据库
        curMy = obj.connMy.cursor()
        curMy.execute("SELECT  UserID  FROM userbasicinfo WHERE UserIDCard = %s", (id_card,))
        result = curMy.fetchone()
        PrintLog('info', '[%s] 通过身份证号获得userid: result: %s', threading.currentThread().getName(), result)
        if result is None:
            return []
        userid = result[0]

        db = obj.conn[obj.dbname]      #选择mongodb数据库
        account = db['userlabelquery']
        query_where = {}
        query_where['userId'] = userid
        result = account.find_one(query_where)
        PrintLog('info', '[%s] 通过身份证号获得标签id: result: %s', threading.currentThread().getName(), result)
        if result is not  None:
            result = map(int,result['labelIds'])
        else:
            result = []
        return result


    def _gettotalnum_intersect(self, obj, label_ids):
        '''
        查询标签对应用户的交集，返回用户数
        '''
        if label_ids == []:
            return 0
        db = obj.conn[obj.dbname]      #选择数据库
        account = db['userlabelquery']
        where = {'labelIds': {'$all':label_ids}}
        count = account.find(where).count()
        return count


    def _gettotalnum_union(self, obj, label_ids):
        '''
        查询标签对应用户的并集，返回用户数
        '''
        if label_ids == []:
            return 0
        db = obj.conn[obj.dbname]      #选择数据库
        account = db['userlabelquery']
        where = {'labelIds': {'$in':label_ids}}
        count = account.find(where).count()
        return count


    def UPSAssert(self, obj, response, paramsDict, ExpectationDict):
        '''
        UPS断言入口
        '''
        try:
            #print 'response apparent_encoding: ', response.apparent_encoding
            #print 'response encoding: ', response.encoding
            response.encoding = response.apparent_encoding
            assert response.status_code == 200, u'HTTP响应码错误'

            responseContent =  unicode(response.content, "utf-8")
            #print 'unicode response.content: %s' % unicode(response.content, "utf-8")
            responseContentDict = json.loads(responseContent)

            if ExpectationDict != '':
                PrintLog('debug','[%s] 比较响应数据与期望数据: responseContentDict: %s  ExpectationDict: %s', threading.currentThread().getName(), responseContentDict, ExpectationDict)
                assert cmp(responseContentDict, ExpectationDict) == 0, u'响应数据与期望不一致'
                return 'PASS',

            function_code = int(paramsDict['function_code'])
            if function_code == 600021:                     #查询用户标签
                assert responseContentDict['result']['result_code'] == 'SUCCESS', u"响应result_code字段检查失败"
                responseLabels_name = responseContentDict['labels']
                PrintLog('debug', '[%s] 响应数据标签名: responseLabels_name: %s', threading.currentThread().getName(), responseLabels_name)
                if responseLabels_name != []:
                    responseLabels = self._labels2id(obj, responseLabels_name)
                else:
                    responseLabels = []

                try:
                    id_card = paramsDict['id_card']
                except KeyError:
                    id_card = False
                try:
                    mobile_phone = paramsDict['mobile_phone']
                except KeyError:
                    mobile_phone = False

                if id_card is not False:
                    expectationLabels = self._getlabels_id_card(obj, id_card)
                    if expectationLabels !=[]:
                        PrintLog('debug', '[%s] 比较响应数据标签与期望标签: responseLabels: %s expectationLabels: %s', threading.currentThread().getName(), responseLabels, expectationLabels)
                        assert len(set(expectationLabels)^set(responseLabels)) == 0, u'响应数据与期望不一致'
                        return 'PASS',

                if mobile_phone is not False:
                    expectationLabels = self._getlabels_mobile_phone(obj, mobile_phone)
                    PrintLog('debug','[%s] 比较响应数据标签与期望标签: responseLabels: %s expectationLabels: %s', threading.currentThread().getName(), responseLabels, expectationLabels)
                    assert len(set(expectationLabels)^set(responseLabels)) == 0, u'响应数据与期望不一致'
                    return 'PASS',
                raise ValueError('Test Data Error')

            if function_code == 600022:  #查询标签对应用户
                assert responseContentDict['result']['result_code'] == 'SUCCESS', u"响应result_code字段检查失败"
                response_total_number = responseContentDict['total_number']
                response_users = responseContentDict['users']
                response_usersN = len(response_users)

                label_ids = paramsDict['label_ids']
                all_in = int(paramsDict['all_in'])
                cur_page = int(paramsDict['cur_page'])
                page_num = int(paramsDict['page_num'])

                if all_in != 1:
                    expectation_total_number = self._gettotalnum_intersect(obj, label_ids)
                else:
                    expectation_total_number = self._gettotalnum_union(obj, label_ids)

                PrintLog('debug', '[%s] 比较响应数据total_number与期望total_number: response_total_number: %s expectation_total_number: %s', threading.currentThread().getName(), response_total_number, expectation_total_number)
                assert expectation_total_number == response_total_number, u'响应total_number字段值不正确'

                PrintLog('debug', '[%s] 检查响应数据users字段数据条数是否正确: response_usersN: %s page_num: %s', threading.currentThread().getName(), response_usersN, page_num)
                if expectation_total_number >= page_num:
                    assert page_num == response_usersN, u'响应users字段数据条数不正确'
                else:
                    assert expectation_total_number == response_usersN, u'响应users字段数据条数不正确'
                return 'PASS',
            raise ValueError('Test Data function_code Error')

        except TableNoneError as e:
            PrintLog('info', '[%s] TableNoneError: TableName: %s', threading.currentThread().getName(), unicode(e))
            return 'NONE',unicode(e)
        except AssertionError as e:
            PrintLog('info', '[%s] AssertionError: %s', threading.currentThread().getName(),unicode(e.args[0]))
            return 'FAIL',unicode(e.args[0])
        except Exception as e:
            PrintLog('exception',e)
            return 'ERROR',unicode(e)
