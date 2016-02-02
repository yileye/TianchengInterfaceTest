#coding=utf8
#######################################################
#filename:GenerateLog.py
#author:defias
#date:2015-10
#function: 生成日志
#######################################################
from Global import *
import logging
import os
import time

class GenerateTxtLog(object):
    '''
    生成txt日志
    '''
    if not os.path.isdir('./log'):
        os.mkdir("./log")
    logf_path = './log/TianchengTest_log.txt'

    @classmethod
    def GenTxtLog(cls):
        '''
        生成日志文件同时输出到控制台
        '''
        global loggerfile, loggercontrol
        loggerfile.setLevel(logging.DEBUG)   #设置日志等级
        loggercontrol.setLevel(logging.DEBUG)

        filename = os.path.basename(cls.logf_path)
        filepath = os.path.dirname(cls.logf_path)
        parent_path, ext = os.path.splitext(filename)
        tm = time.strftime('%Y%m%d%H%M%S', time.localtime())
        #filename = parent_path + tm + ext   #日志文件名中添加当前时间
        filename = parent_path + tm   #日志文件名中添加当前时间

        # handler
        logfile = logging.FileHandler(os.path.join(filepath, filename))
        logfile.setLevel(logging.DEBUG)
        control = logging.StreamHandler()
        control.setLevel(logging.DEBUG)

        # formatter
        #formatter = logging.Formatter('%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s - %(message)s')
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        logfile.setFormatter(formatter)
        control.setFormatter(formatter)

        # bound
        loggercontrol.addHandler(control)    #日志输出到控制台
        loggerfile.addHandler(logfile)    #日志输出到文件
