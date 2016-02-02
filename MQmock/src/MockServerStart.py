#coding=utf8
from Global import *
import Config
import MockMQServer
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
        MQData_IDs = MockData.MockDataXls.get_sheetAllID()
        PrintLog('debug', 'MQData_IDs: %s', MQData_IDs)
        MQD_ID_Key = ModMockO.MQData_ID_Key(MQData_IDs)
        if MQD_ID_Key is False:
            raise ValueError(u'HttpData存在重复数据！！！')
        PrintLog('debug', 'MQD_ID_Key: %s', MQD_ID_Key)
        MQMEMdata.write(ch2unicode(MQD_ID_Key))         #HttpD_ID_Key写入内存

        #启动HTTP服务子进程
        MQServerO = MockMQServer.MQServer()
        MQServerO.run()

    except ValueError as e:
        print unicode(e.args[0])
    except Exception as e:
        print unicode(e)
