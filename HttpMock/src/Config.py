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
    def get_datafilename(cls):
        '''
        获取数据文件名称
        '''
        return cls.confO.get('DEFAULT', 'datafilename')

    @classmethod
    def get_mockdata_col(cls):
        '''
        获取数据文件列定义
        '''
        return cls.confO.get('DEFAULT', 'mockdata_col')

    @classmethod
    def get_host(cls):
        '''
        获取主机名
        '''
        return cls.confO.get('DEFAULT', 'host')

    @classmethod
    def get_port(cls):
        '''
        获取端口号
        '''
        return int(cls.confO.get('DEFAULT', 'port'))

    @classmethod
    def get_TestEnvironment_Info(cls, section, field):
        '''
        获取环境信息
        '''
        return cls.confO.get(section, field)
