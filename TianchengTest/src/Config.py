#coding=utf8
#######################################################
#filename:Config.py
#author:defias
#date:2015-11
#function: 配置类
#######################################################
import configparser
import codecs
import os

class ConfigIni(object):
    '''
    配置类
    '''
    if not os.path.isfile('./Config.ini'):
        raise Exception, u'Don\'t find config file: Config.ini'
    conf_path = './Config.ini'
    confO = configparser.ConfigParser()
    confO.readfp(codecs.open(conf_path, "r", "utf-8"))

    @classmethod
    def get_TestcaseName(cls):
        '''
        获取测试用例名
        '''
        return cls.confO.get('DEFAULT', 'TestcaseName')

    @classmethod
    def get_runmode(cls):
        '''
        获取运行模式
        '''
        return cls.confO.get('DEFAULT', 'runmode')

    @classmethod
    def get_iscontrol(cls):
        '''
        获取日志控制开关
        '''
        return cls.confO.get('DEFAULT', 'iscontrol')

    @classmethod
    def get_isstdebug(cls):
        '''
        获取sublime text debug开关
        '''
        return cls.confO.get('DEFAULT', 'isstdebug')

    @classmethod
    def get_index(cls):
        '''
        获取待执行的用例
        '''
        return cls.confO.get('DEFAULT', 'index')

    @classmethod
    def get_unindex(cls):
        '''
        获取不执行的用例
        '''
        return cls.confO.get('DEFAULT', 'unindex')

    @classmethod
    def get_testcase_col(cls):
        '''
        获取用例文件列定义
        '''
        return cls.confO.get('DEFAULT', 'testcase_col')

    @classmethod
    def get_TestEnvironment_Info(cls, section, field):
        '''
        获取UBAS测试环境信息
        '''
        return cls.confO.get(section, field)
