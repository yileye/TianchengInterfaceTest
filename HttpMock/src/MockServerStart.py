#coding=utf8
from Global import *
import Config
import MockHttpServer
from GenerateLog import GenerateTxtLog
import ModMock
import MockData
import time


def MockServerStart():
    '''
    测试主流程
    '''
    try:
        #启动日志
        GenerateTxtLog.GenTxtLog()
        ModMockO = ModMock.ModMock()

        #HttpD_ID_Key写入内存
        HttpData_IDs = MockData.MockDataXls.get_sheetAllID()
        PrintLog('debug', 'HttpData_IDs: %s', HttpData_IDs)
        HttpD_ID_Key = ModMockO.HttpData_ID_Key(HttpData_IDs)
        if HttpD_ID_Key is False:
            raise ValueError(u'HttpData存在重复数据！！！')
        PrintLog('debug', 'HttpD_ID_Key: %s', HttpD_ID_Key)
        HttpMEMdata.write(ch2unicode(HttpD_ID_Key))         #HttpD_ID_Key写入内存

        #启动HTTP服务子进程
        HttpServerO = MockHttpServer.HttpServer()
        HttpServerO.run()

    except ValueError as e:
        print unicode(e.args[0])
    except Exception as e:
        print unicode(e)
