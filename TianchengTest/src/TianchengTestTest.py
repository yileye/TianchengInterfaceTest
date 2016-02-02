#coding=utf8
#######################################################
#filename:TianchengTestTest.py
#author:defias
#date:2015-11
#function: 测试
#######################################################
import unittest
import logging
from public import Configfile_Parser

#+++++++++++++++++++++++++++++++++++++++++++++++++++++
import Config
import TestCase
import GenerateLog

from Global import *
import Interface_Driver
import GenerateReport

import Interface_Driver
from public import ExcelRW
import TianchengTest

class TianchengTestTest(unittest.TestCase):
    def setUp(self):
        GenerateLog.GenerateTxtLog.GenTxtLog()
        pass

    def tearDown(self):
        pass

    def ntest_Interface_DoData_insert(self):
        conf_file = '..\\Conf.ini'
        #读配置文件
        confeng = Configfile_Parser.Configfile_Parser(conf_file)
        section = 'UPSDB_INSERT'
        params = '{"ytest":{"a":"2015-10-12", "b":"bbb1", "c":"ccc1", "d":"ddd1"}}'
        DoDataO = Interface_Driver.Interface_DoData(confeng, section)
        DoDataO.insert(params)

    def ntest_Interface_DoData_paramskong(self):
        conf_file = '..\\Conf.ini'
        confeng = Configfile_Parser.Configfile_Parser(conf_file)
        section = 'UPSDB_INSERT'
        params = '{}'
        DoDataO = Interface_Driver.Interface_DoData(confeng, section)
        DoDataO.insert(params)

    def ntest_Interface_DoData_ziduankong(self):
        conf_file = '..\\Conf.ini'
        confeng = Configfile_Parser.Configfile_Parser(conf_file)
        section = 'UPSDB_INSERT'
        params = '{"ytest":{}}'
        DoDataO = Interface_Driver.Interface_DoData(confeng, section)
        DoDataO.insert(params)

    def ntest_HtmlReport(self):
        testcase_result = {('UPS',2):(u'FAIL失败',u'FAIL 撒的发生info'), ('UPS',1):('FAILS','sadfsfasdf')}
        HtmlReportO = GenerateReport.HtmlReport(testcase_result, 100)
        HtmlReportO.generate_html()

    def ntest_ConfigIni_TestEnvironment_Info(self):
        Info = Config.ConfigIni.get_TestEnvironment_Info('UPS', 'userdb_host')
        print Info
        self.assertEqual(Info, u"192.168.18.69")

    def ntest_ConfigIni_TestEnvironment_Info(self):
        Info = Config.ConfigIni.get_TestEnvironment_Info('UPS', 'userdb_port')
        print Info
        self.assertEqual(Info, u"3306")

    def ntest_ConfigIni_index(self):
        index = Config.ConfigIni.get_index()
        print type(eval(index))
        print index

    def ntest_TestCaseXls_TestType(self):
        print TestCase.TestCaseXls.get_TestType('UPS', 1)
        self.assertEqual(TestCase.TestCaseXls.get_TestType('UPS', 1), u'用户属性标签')

    def ntest_TestCaseXls_Expectation(self):
        print TestCase.TestCaseXls.get_Expectation('UPS', 1)
        self.assertEqual(TestCase.TestCaseXls.get_Expectation('UPS', 1), u'{"Expectation":1010001}')

    def ntest_TestCaseXls_Testid2rown(self):
        self.assertEqual(TestCase.TestCaseXls.Testid2rown('UPS', 1), 1)

    def ntest_TestCaseXls_Alltestid_nosheet(self):
        print TestCase.TestCaseXls.get_Alltestid(['UPSLabel','UPS'])

    def ntest_TianchengTest_getModTestid(self):
        print TianchengTest.getModTestid(2)



    def ntest_GenerateTxtLog_GenTxtLog(self):
        GenerateLog.GenerateTxtLog.GenTxtLog()
        logger.debug('testing')

    def ntest_Interface_Http_get(self):
        url = 'http://192.168.18.77:8080/'
        HttpO = Interface_Driver.Interface_Http(url)
        r = HttpO.get()
        self.assertEqual(r.status_code, 200)

    def ntest_Interface_Http_post(self):
        url = 'http://192.168.18.77:8080/uap/api/ups'
        headers = {"APPID":"10","TOKEN":"abcdefghijk"}
        params = '{"function_code":"600021","id_card":"320721199110094227"}'
        HttpO = Interface_Driver.Interface_Http(url)
        r = HttpO.post(headers, params)
        self.assertEqual(r.status_code, 200)

    def ntest_Interface_DoData_insert(self):
        dbinfo = ('192.168.18.69', 3306, 'root', 'niiwooroot', 'ubas_tianchengtest')
        params = u'{"ytest":{"a":"2015-11-4", "b":"bbb1", "c":"ccc1", "d":"ddd1"}}'
        DoDataO = Interface_Driver.Interface_DoData(dbinfo)
        self.assertTrue(DoDataO.insert(params))

    def ntest_ExcelRW(self):
        xlseng = ExcelRW.XlsEngine('..\\TestCase.xlsx')
        print type(xlseng.getsheets())
        print xlseng.getrows('UPS')
        print xlseng.getcols('UPS')
        print xlseng.readrow('UPS', 0)
        print xlseng.readcol('UPS', 0)
        print xlseng.readcell('UPS',1,1)



if __name__ == '__main__':
    unittest.main()
