#coding=utf8
from Global import *
import Mock_HttpServer, Config
from GenerateLog import GenerateTxtLog
import threading
import time

def testHttpServer():
    #启动日志
    GenerateTxtLog.GenTxtLog()

    iscontrol = str(Config.ConfigIni.get_iscontrol())
    isstdebug = str(Config.ConfigIni.get_isstdebug())
    memdata.write(ch2unicode(iscontrol + '\n' + isstdebug))  #写入内存

    HttpServerO = Mock_HttpServer.HttpServer()
    HttpServerO.Start()


def testHttpServer2():
    #启动日志
    GenerateTxtLog.GenTxtLog()

    iscontrol = str(Config.ConfigIni.get_iscontrol())
    isstdebug = str(Config.ConfigIni.get_isstdebug())
    memdata.write(ch2unicode(iscontrol + '\n' + isstdebug))  #写入内存
    HttpServerO = Mock_HttpServer.HttpServer()

    HttpServerTh = threading.Thread(target=HttpServerO.Start,name='HttpServer')
    HttpServerTh.setDaemon(True)
    HttpServerTh.start()
    print 1111
    time.sleep(5)
    print 2222

