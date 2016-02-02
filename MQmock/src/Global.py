#coding=utf8
#######################################################
#filename:Global.py
#author:defias
#date:2015-10
#function: 全局变量和通用功能函数
#######################################################
import logging
import platform
from io import StringIO
import inspect
import os

#日志
loggerfile = logging.getLogger('logfile')
loggercontrol = logging.getLogger('control')

#内存数据
MQMEMdata = StringIO()

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
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

def ch2s(s):
    '''
    写字符串时针对不同系统的编码转换
    '''
    systype = platform.system()
    if systype == 'Windows':
        us = ch2unicode(s)
        return us.encode('gbk')
    if systype == 'Linux':
        us = ch2unicode(s)
        return us.encode('utf-8')
    else:
        return s

def PrintLog(loglevel, fixd, *data):
    '''
    打印日志
    '''
    global loggerfile, loggercontrol
    iscontrol = 1
    isstdebug = 0
    if loglevel == 'exception':
        getattr(loggerfile, loglevel)(fixd)
        if iscontrol != 0:
            getattr(loggercontrol, loglevel)(fixd)
    else:
        systype = platform.system()
        if systype == 'Windows' and isstdebug == 0:
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

class TableNoneError(MyError):
    '''
    自定义TableNone异常类
    '''
    pass



if __name__ == '__main__':
    pass
