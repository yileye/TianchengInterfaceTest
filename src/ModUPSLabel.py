#coding=utf8
#######################################################
#filename:ModUPS.py
#author:defias
#date:2015-11
#function: UPS相关
#######################################################
from Global import *
import threading
import Config
import uuid
import json

class ModUPSLabel(object):
    def __init__(self):
        pass

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

    def getRuncaseEnvironment_Timeouttask_label(self, TestEnvironment):
        '''
        获取环境信息: timeouttask_label
        '''
        try:
            timeouttask_label = Config.ConfigIni.get_TestEnvironment_Info(TestEnvironment, 'timeouttask_label')
        except:
            return 0
        return timeouttask_label

    def getRuncaseEnvironment_Timeoutdelay_label(self, TestEnvironment):
        '''
        获取环境信息:timeoutdelay_label
        '''
        try:
            timeoutdelay_label = Config.ConfigIni.get_TestEnvironment_Info(TestEnvironment, 'timeoutdelay_label')
        except:
            return 0
        return timeoutdelay_label

    def parseExpForDriver(self, Expectation):
        '''
        解析期望结果获取用例执行所需数据
        '''
        try:
            ExpectationDict = json.loads(Expectation)
            if len(ExpectationDict) != 1:
                raise ValueError
            if u"Expectation" == ExpectationDict.keys()[0]:
                isdelaytime = False
            if u"!Expectation" == ExpectationDict.keys()[0]:
                isdelaytime = True
            return isdelaytime
        except Exception as e:
            PrintLog('exception',e)
            raise

    def parseParamsForDriver(self, params):
        '''
        解析测试数据获取用例执行所需数据
        '''
        try:
            params_dict = json.loads(params)
            params_result = []
            tables = params_dict.keys()
            for table in tables:
                fields = params_dict[table].keys()
                values = params_dict[table].values()
                params_result.append((table, fields, values))
            return params_result
        except Exception as e:
            PrintLog('exception',e)
            return False

    def parseExpForAssert(self, Expectation):
        '''
        解析期望结果获取断言所需数据
        '''
        try:
            ExpectationDict = json.loads(Expectation)
            if len(ExpectationDict) != 1:
                raise ValueError
            if u"Expectation" == ExpectationDict.keys()[0]:
                isdelaytime = False
                values = ExpectationDict["Expectation"]
            if u"!Expectation" == ExpectationDict.keys()[0]:
                isdelaytime = True
                values = ExpectationDict["!Expectation"]
            return isdelaytime,values
        except Exception as e:
            PrintLog('exception',e)
            raise

    def DriverCbFunction(self, params_result):
        '''
        Driver回调函数
        '''
        userid = 'AutoTest123456-' + str(uuid.uuid1())   #唯一userid
        nows = gettime_nowstamp()  #当前时间戳
        notltimetables = ['loginevent','postlianlianrechargeevent','postguaranteeevent','postpublishborrowmoneyevent','postinvestmentevent'] #无需增加LastUpdateTime字段的表
        mustbidtables = ['bidbasicinfo', 'investinfo', 'loaninfo', 'diligenceinfo']
        chtimefields =  ['RegisterTime', 'EventTimestmap', 'LastUpdateTime']    #需要转换为时间戳的列

        userbasicinfo_mustcol = ['UserId', 'UserType', 'UserStatus', 'LastUpdateTime']
        userbasicinfo_mustvalue = [userid,1,0,nows]

        #修正字段和值
        for i in xrange(len(params_result)):
            table = params_result[i][0]
            fields = params_result[i][1]
            values = params_result[i][2]
            #无UserId字段的添加UserId字段
            if 'UserId' not in fields:
                fields.insert(0, 'UserId')
                values.insert(0, userid)

            #添加LastUpdateTime字段
            if table not in notltimetables:
                if 'LastUpdateTime' not in fields:
                    fields.append('LastUpdateTime')
                    values.append(nows)

            #添加Bid字段
            if table in mustbidtables:
                if 'Bid' not in fields:
                    fields.append('Bid')
                    values.append(userid)

            #添加UserName字段
            if table == 'loginevent':
                if 'UserName' not in fields:
                    fields.append('UserName')
                    values.append('testusername')

            #添加UserType,UserStatus字段
            if table == 'userbasicinfo':
                if 'UserType' not in fields:
                    fields.append('UserType')
                    values.append(1)
                if 'UserStatus' not in fields:
                    fields.append('UserStatus')
                    values.append(0)

            #字符串时间转换为时间戳
            for f in range(len(fields)):
                field = fields[f]
                value = values[f]
                if field in chtimefields and type(value) is unicode:
                    value = change_time(value)
                    values[f] = value

            #更新params_result
            params_result.pop(i)
            params_result.insert(i,(table, fields, values))

        #增加主表userbasicinfo
        tables = map(lambda x: x[0], params_result)
        if tables == [] or "userbasicinfo" not in tables:
            params_result.insert(0, ("userbasicinfo", userbasicinfo_mustcol, userbasicinfo_mustvalue))
        return params_result,userid

    def AssertCbFunction(self, expectation, taskargs):
        '''
        Assert回调函数
        '''
        #expectation: {"Expectation":[1010001]}
        #newexpectation: {"userlabelquery":{"labelIds":[1010001]}, "userlabel":{"labelIds":[1010001]}}
        parseResult = self.parseExpForAssert(expectation)
        value = parseResult[1]
        if parseResult[0] is False:
            newexpectation = {'userlabelquery':{'labelIds':value}, 'userlabel':{'labelIds':value}}
        else:
            newexpectation = {'!userlabelquery':{'labelIds':value}, '!userlabel':{'labelIds':value}}
        return (newexpectation, taskargs)


class ModUPSLabel_Assert(object):
    '''
    UPSLabel断言
    '''
    def __init__(self):
        pass

    def _checkLabel(self, obj, values, userid):
        '''
        检查标签
        '''
        where = {'userId': userid}

        #userlabelquery表
        value = values[0]
        db = obj.conn[obj.dbname]      #选择数据库
        account = db['userlabelquery']
        field =  value.keys()[0]
        explabels = value[field]

        findrt = account.find_one(where)
        PrintLog('debug', '[%s] userlabelquery表检查结果: %s', threading.currentThread().getName(), findrt)
        if findrt is None:
            raise  TableNoneError(u"userlabelquery is None")
        resultset = set(findrt[field])
        assert set(explabels).issubset(resultset), u'userlabelquery表中数据与期望不一致'


        #userlabel表
        value = values[1]
        account = db['userlabel']
        field =  value.keys()[0]
        explabels = value[field]

        resultlist = []
        result = account.find(where)
        if result is None:
            raise  TableNoneError(u"userlabel is None")
        for item in result:
            for i in item[field]:
                resultlist.append(i)
        PrintLog('debug', '[%s] userlabel表检查结果: %s', threading.currentThread().getName(), resultlist)
        resultset = set(resultlist)
        assert set(explabels).issubset(resultset), u'userlabel表中数据与期望不一致'



    def _checkNotLabel(self, obj, values, userid):
        '''
        检查无标签
        '''
        where = {'userId': userid}

        #userlabelquery表
        value = values[0]
        db = obj.conn[obj.dbname]      #选择数据库
        account = db['userlabelquery']  #选择表
        field =  value.keys()[0]
        explabels = value[field]

        findrt = account.find_one(where)
        PrintLog('debug', '[%s] userlabelquery表检查结果: %s', threading.currentThread().getName(), findrt)
        if findrt is not None:
            resultset = set(findrt[field])
            for i in explabels:
                assert not set([i]).issubset(resultset), u'userlabelquery表中数据与期望不一致'


        #userlabel表
        value = values[1]
        account = db['userlabel']
        field =  value.keys()[0]
        explabels = value[field]

        resultlist = []
        result = account.find(where)
        PrintLog('debug', '[%s] userlabel表查询结果result: %s', threading.currentThread().getName(), result)
        if result is not None:
            for item in result:
                if item.has_key(field):
                    for i in item[field]:
                        resultlist.append(i)
            resultset = set(resultlist)

            for i in explabels:
                assert not set([i]).issubset(resultset), u'userlabel表中数据与期望不一致'


    def UPSLabelAssert(self, obj, expectation, userid):
        '''
        UPSLabel断言入口
        '''
        #expectation: {"userlabelquery":{"labelIds":[1010001]}, "userlabel":{"labelIds":[1010001]}}
        try:
            tables = []
            values = []
            for table in expectation:
                tables.append(table)
                values.append(expectation[table])

            if set(tables) == set(["userlabelquery", "userlabel"]):
                PrintLog('debug', '[%s] 调用标签检查函数: _checkLabel  参数:%s', threading.currentThread().getName(), (obj, values, userid))
                self._checkLabel(obj, values, userid)
            if set(tables) == set(["!userlabelquery", "!userlabel"]):
                PrintLog('debug', '[%s] 调用标签检查函数: _checkNotLabel  参数: %s', threading.currentThread().getName(), (obj, values, userid))
                self._checkNotLabel(obj, values, userid)
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
