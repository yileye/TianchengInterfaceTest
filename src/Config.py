#coding=utf8
#######################################################
#filename:Config.py
#author:defias
#date:2015-11
#function: 配置类
#######################################################
import configparser

class ConfigIni(object):
    '''
    配置类
    '''
    conf_path = '.\\Config.ini'
    confO = configparser.ConfigParser()
    confO.read(conf_path)

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
    def get_isrelease(cls):
        '''
        获取发布控制开关
        '''
        return cls.confO.get('DEFAULT', 'isrelease')


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
