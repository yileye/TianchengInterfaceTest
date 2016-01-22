#coding=utf8
#######################################################
#filename:TianchengTest.py
#author:defias
#date:2015-11
#function:
#######################################################
from Global import *
import Config
import TestCase
from GenerateLog import GenerateTxtLog
from GenerateReport import HtmlReport
from Interface_DriverEngine import Interface_DriverEngine
from Interface_AssertEngine import Interface_AssertEngine

import threading
import Queue
import time

def getModTestid(Mode):
    '''
    根据执行模式获取待执行用例testid
    '''
    Allsheets = TestCase.TestCaseXls.get_CaseSheets()
    if Mode == 1:
        PrintLog('debug', '运行模式：部分执行')
        index = eval(Config.ConfigIni.get_index())
        for sheet in index:
            if sheet not in Allsheets:
                raise ValueError, u'index配置错误:Errorindex: %s' % str(index)
        if index != {}:
            nullsheets = [x for x in index.keys() if index[x] == []]
            for i in nullsheets:
                del index[i]
            nullindex = TestCase.TestCaseXls.get_Alltestid(nullsheets)
            index.update(nullindex)
        TestIds = index

    elif Mode == 2:
        PrintLog('debug', '运行模式：部分不执行')
        unindex = eval(Config.ConfigIni.get_unindex())
        for sheet in unindex:
            if sheet not in Allsheets:
                raise ValueError, u'unindex配置错误:Errorunindex: %s' % str(unindex)

        TestIds = TestCase.TestCaseXls.get_Alltestid()
        if unindex != {}:
            nullsheets = [x for x in unindex.keys() if unindex[x] == []]
            for i in nullsheets:
                del TestIds[i]
                del unindex[i]
            for sheet in unindex:
                for testid in unindex[sheet]:
                    TestIds[sheet].remove(testid)

    elif Mode == 0:
        PrintLog('debug', '运行模式：全部分执行')
        TestIds = TestCase.TestCaseXls.get_Alltestid()
    else:
        raise ValueError, u'Mode配置错误:ErrorMode: %d' % Mode
    return TestIds



class TestAssertThread(threading.Thread):
    '''
    断言任务子线程
    '''
    def __init__(self, tdname, tresult_qlock):
        threading.Thread.__init__(self, name=tdname)
        global taskassert_queue
        global testcase_result
        self.tresult_qlock = tresult_qlock
        self.AssertEngineO = Interface_AssertEngine()
        self.timestate = {}
        self.timeevery = 5

    def run(self):
        while True:
            try:
                task = taskassert_queue.get(block=True, timeout=15)
                PrintLog('debug', '[%s] 从队列taskassert_queue中取出一条任务: %s', self.getName(), task)
                taskassert_queue.task_done()

                sheet,testid,timeouttask,timeoutdelay,taskargs = task
                nowtimestamp = getnowstamp()

                #时间状态处理
                if (sheet,testid) in self.timestate:
                    if self.timestate[(sheet,testid)]['timeoutdelay'] > 0.0:
                        DiffTime = nowtimestamp - timeoutdelay
                        timeoutdelay_update = self.timestate[(sheet,testid)]['timeoutdelay'] - DiffTime
                        if timeoutdelay_update <= 0.0:
                            self.timestate[(sheet,testid)]['timeoutdelay'] = 0.0
                        else:
                            self.timestate[(sheet,testid)]['timeoutdelay'] = timeoutdelay_update
                    if self.timestate[(sheet,testid)]['timeouttask'] > 0.0:
                        DiffTime = nowtimestamp - timeouttask
                        timeouttask_update = self.timestate[(sheet,testid)]['timeouttask'] - DiffTime
                        if timeouttask_update <= 0.0:
                            self.timestate[(sheet,testid)]['timeouttask'] = 0.0
                        else:
                            self.timestate[(sheet,testid)]['timeouttask'] = timeouttask_update
                else:                                               #首次取到该任务
                    self.timestate[(sheet,testid)] = {'timeoutdelay':float(timeoutdelay), 'timeouttask':float(timeouttask)}
                PrintLog('debug', '[%s] 状态处理后timestate: %s', self.getName(), self.timestate)

                #任务处理
                if self.timestate[(sheet,testid)]['timeoutdelay'] > 0.0:      #需要继续延时处理
                    task = sheet,testid,nowtimestamp,nowtimestamp,taskargs
                    PrintLog('debug', '[%s] 放回队列继续处理: %s', self.getName(), task)
                    taskassert_queue.put(task)  #放回队列继续处理
                else:
                    PrintLog('debug', '[%s] 调用断言模块进行处理: %s %s %s', self.getName(), sheet, testid, taskargs)
                    AssertResult = self.AssertEngineO.AssertTestCase(sheet, testid, taskargs)

                    if AssertResult[0] != 'NONE' or self.timestate[(sheet,testid)]['timeouttask'] <= 0.0:   #断言结果为PASS或FAIL或ERROR或超时时间到
                        self.tresult_qlock.acquire()
                        try:
                            PrintLog('debug', '[%s] 结果放入测试结果中: %s %s %s\n...', self.getName(), sheet, testid, AssertResult)
                            testcase_result[(sheet, testid)] = AssertResult    #结果放入测试结果中
                        finally:
                            self.tresult_qlock.release()
                    else:                                      #断言结果为NONE且超时时间未到继续处理
                        nowtimestamp = getnowstamp()
                        task = sheet,testid,nowtimestamp,nowtimestamp,taskargs
                        PrintLog('debug', '[%s] 放回队列继续处理: %s\n...', self.getName(), task)
                        taskassert_queue.put(task)  #放回队列继续处理
                time.sleep(self.timeevery)

            except Queue.Empty:
                PrintLog('debug', '[%s] 从队列taskassert_queue中取任务超时', self.getName())
                break
            except Exception as e:
                PrintLog('exception',e)
                break

class TestRunThread(threading.Thread):
    '''
    执行用例子线程
    '''
    def __init__(self, tdname, tresult_qlock, TestIds):
        threading.Thread.__init__(self, name=tdname)
        global testcase_result
        self.tresult_qlock = tresult_qlock
        self.TestIds = TestIds
        self.DriverEngineO = Interface_DriverEngine()
        self.timeevery = 1

    def run(self):
        for sheet in self.TestIds:
            for testid in self.TestIds[sheet]:
                PrintLog('debug', '[%s] 开始执行用例: (%s, %s)\n---', self.getName(), sheet, testid)
                if self.DriverEngineO.RunTestCase(sheet, testid) is False:
                    self.tresult_qlock.acquire()
                    try:
                        PrintLog('debug', '[%s] 测试操作不成功: (%s, %s)', self.getName(), sheet, testid)
                        testcase_result[(sheet, testid)] = ('ERROR',u'测试操作不成功')
                    finally:
                        self.tresult_qlock.release()
                time.sleep(self.timeevery)

def TianchengTest():
    '''
    测试主流程
    '''
    try:
        #启动日志
        GenerateTxtLog.GenTxtLog()

        #获取运行模式
        runmode = int(Config.ConfigIni.get_runmode())
        iscontrol = str(Config.ConfigIni.get_iscontrol())
        isstdebug = str(Config.ConfigIni.get_isstdebug())
        memdata.write(ch2unicode(iscontrol + '\n' + isstdebug))  #写入内存

        #锁
        tresult_qlock = threading.Lock()

        #全局变量
        global testcase_result
        global taskassert_queue

        #记录测试开始时间
        start_time = getnowstamp()
        start_now = getnowtime()
        PrintLog('debug', '测试开始时间: %s', start_now)

        #获取待执行用例
        TestIds = getModTestid(runmode)
        PrintLog('debug', '待执行用例: %s', TestIds)

        #启动执行子线程
        PrintLog('debug', 'Starting thread: TestRunThread')
        Thread_runO = TestRunThread('TestRunThread', tresult_qlock, TestIds)
        Thread_runO.setDaemon(True)
        Thread_runO.start()
        time.sleep(1)

        #启动断言子线程
        PrintLog('debug', 'Starting thread: TestAssertThread')
        Thread_assertO = TestAssertThread('TestAssertThread', tresult_qlock)
        Thread_assertO.setDaemon(True)
        Thread_assertO.start()


        #等待断言子线程结束
        PrintLog('debug', '等待子线程TestRunThread结束...')
        Thread_runO.join()
        PrintLog('debug', '子线程：TestRunThread结束')

        PrintLog('debug', '等待子线程TestAssertThread结束...')
        Thread_assertO.join()
        PrintLog('debug', '子线程：TestAssertThread结束')

        #等待任务队列为空
        #taskassert_queue.join()

        #测试结束时间
        end_time = getnowstamp()
        end_now = getnowtime()
        PrintLog('debug', '测试结束时间: %s', end_now)

        #生成测试报告
        PrintLog('debug', 'testcase_result: %s', testcase_result)
        HtmlReportO = HtmlReport(testcase_result, end_time-start_time)
        HtmlReportO.generate_html()

    except ValueError as e:
        print unicode(e.args[0])
    except Exception as e:
        print unicode(e)
