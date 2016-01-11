#coding=utf8
#######################################################
#filename:Global.py
#author:defias
#date:2015-10
#function: 全局变量和通用功能函数
#######################################################
import logging
import json
import time, datetime
import Queue
import platform
from io import StringIO
import inspect
import os

#日志
global logger
loggerfile = logging.getLogger('logfile')
loggercontrol = logging.getLogger('control')

#断言异步任务队列
global taskassert_queue
taskassert_queue = Queue.Queue()  #断言任务队列

#保存测试结果
global testcase_result
testcase_result = {}

#内存数据
memdata = StringIO()

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def package_taskdelay(task, delaytime, callback):
    '''
    封装延时任务队列(队列项)
    '''
    delaytask = {
        'delaytask': delaytask,
        'delaytime': delaytime,
        'callback': callback   #延时后的处理函数
    }
    return delaytask


def change_tablename(params,tablename):
    '''
    变更表名:表名添加operateTime日期
    '''
    params_dict = json.loads(params.decode('gbk'))   #解析期望结果数据
    operateTime = params_dict['operateTime']
    operateDate = operateTime.split(' ')[0]
    for operateDate_s in operateDate.split('-'):
        operateDate_s = '' + operateDate_s
    tablename = tablename + operateDate_s
    return tablename

def change_time(time_str):
    '''
    将%Y-%m-%d格式时间字符串转化为时间戳（带微秒）
    '''
    timeArray = time.strptime(time_str, "%Y-%m-%d")
    timeStamp = int(time.mktime(timeArray))
    timeStamp = int(str(timeStamp) + '000000')
    return timeStamp


def gettime_nowstamp():
    '''
    获取当前包含微秒位的时间戳
    '''
    dnow = datetime.datetime.now()
    dnows = str(int(time.mktime(dnow.timetuple())))
    #mics = str(dnow.microsecond)
    mics = '000000'
    nows = int(dnows + mics)
    return nows


def getnowtime():
    '''
    获取当前%Y-%m-%d %H:%M:%S格式时间
    '''
    nows = time.strftime("%Y-%m-%d %H:%M:%S")
    return nows


def getnowstamp():
    '''
    获取当前时间戳
    '''
    return time.time()


def ch2unicode(data):
    '''
    转换为unicode
    '''
    if type(data) is unicode:
        return data
    if type(data) is not str:
        data = str(data)
    try:
        data = unicode(data, 'utf-8')
    except UnicodeDecodeError:
        data = unicode(data, 'gbk')
    return data


def PrintLog(loglevel, fixd, *data):
    '''
    打印日志
    '''
    iscontrol = int(memdata.getvalue().split()[0])
    isrelease = int(memdata.getvalue().split()[1])       #是否发布
    if loglevel == 'exception':
        getattr(loggerfile, loglevel)(fixd)
        if iscontrol != 0:
            getattr(loggercontrol, loglevel)(fixd)
    else:
        systype = platform.system()
        if systype == 'Windows' and isrelease == 1:
            enty = 'gbk'
        else:
            enty = 'utf-8'

        #获取调用函数的文件名和行号
        filepath = inspect.stack()[1][1]
        filename = os.path.basename(filepath)
        linen = inspect.stack()[1][2]
        fixdd = u'%s[%d] - '

        fixdf = (fixdd + ch2unicode(fixd)).encode('utf-8')
        fixdc = (fixdd + ch2unicode(fixd)).encode(enty)
        valuesf = [filename,linen]
        valuesc = [filename,linen]
        for d in data:
            df = ch2unicode(d).encode('utf-8')
            dc = ch2unicode(d).encode(enty)
            valuesf.append(df)
            valuesc.append(dc)
        getattr(loggerfile, loglevel)(fixdf % tuple(valuesf))
        if iscontrol != 0:
            getattr(loggercontrol, loglevel)(fixdc % tuple(valuesc))


class MyError(Exception):
    '''
    自定义异常类
    '''
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)




if __name__ == '__main__':
    pass
