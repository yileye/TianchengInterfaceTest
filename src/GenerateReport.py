#coding=utf8
#######################################################
#filename:GenerateReport.py
#author:defias
#date:2015-7
#function: 生成报告
#######################################################
from Global import *
from public import pyh
import TestCase
import time
import os
import traceback


class HtmlReport(object):
    '''
    HTML测试报告
    '''
    def __init__(self, testcase_result, seconds):
        self.title = 'Test Report Page'       #网页标签名称
        self.filename = ''                    #结果文件名
        self.time_took = '00:00:00'           #测试耗时
        self.success_num = 0                  #测试通过的用例数
        self.fail_num = 0                     #测试失败的用例数
        self.error_num = 0                    #运行出错的用例数
        self.case_total = 0                   #运行测试用例总数
        self.report_title = ch2s(u'天秤自动化测试报告')
        self.testcase_result = testcase_result   #测试结果 {('UPS', 1):('ERROR','error')}
        self.seconds = seconds         #耗时

    def _setfilename(self):
        '''
        设置结果文件名
        '''
        if not os.path.isdir('./result'):
            os.mkdir("./result")
        filename = './result/Test_Report_Filename.html'
        if os.path.isdir(filename):
            raise IOError("%s must point to a file" % path)
        elif '' == filename:
            raise IOError('filename can not be empty')
        else:
            parent_path, ext = os.path.splitext(filename)
            tm = time.strftime('%Y%m%d%H%M%S', time.localtime())
            self.filename = parent_path + tm + ext   #报告名中添加当前时间
        return True

    def generate_html(self):
        '''
        生成HTML报告
        '''
        #解析测试结果
        try:
            case_total = len(self.testcase_result)
            success_num = len([x for x in self.testcase_result.values() if x[0] in ['PASS']])
            fail_num = len([x for x in self.testcase_result.values() if x[0] in ['FAIL']])
            error_num = case_total - success_num - fail_num
        except:
            case_total = 0
            success_num = 0
            fail_num = 0
            error_num = 0

        #生成测试概况
        page = pyh.PyH(self.title)
        page << pyh.h1(self.report_title, align='middle') #标题居中
        page << pyh.p(ch2s(u'测试总耗时：') + str(time.strftime('%H:%M:%S', time.gmtime(self.seconds))))
        page << pyh.p(ch2s(u'测试用例总数：') + str(case_total))
        page << pyh.p(ch2s(u'成功用例数：') + str(success_num))
        page << pyh.p(ch2s(u'失败用例数：') + str(fail_num))
        page << pyh.p(ch2s(u'出错用例数：') + str(error_num))

        #设置表格属性
        tab = page << pyh.table()
        tab.attributes['border'] = '1'   #表格边框
        tab.attributes['cellpadding'] = '1'   #单元格边沿与其内容之间的空白
        tab.attributes['cellspacing'] = '0'   #单元格之间间隔
        tab.attributes['cl'] = 'table'
        tab.attributes['borderColor'] = '#504F4F'
        tab.attributes['width'] = '90%'

        #生成表格头
        tab << pyh.tr(pyh.th(ch2s(u'用例ID'), bgcolor='#E6E6FA', align='left') + pyh.th(ch2s(u'用例名称'), bgcolor='#E6E6FA', align='left') +
            pyh.th(ch2s(u'测试项'), bgcolor='#E6E6FA', align='left') + pyh.th(ch2s(u'测试项类型'), bgcolor='#E6E6FA', align='left') +
            pyh.th(ch2s(u'测试结果'), bgcolor='#E6E6FA', align='left') + pyh.th(ch2s(u'提示信息'), bgcolor='#E6E6FA', align='left'))

        #填表格
        testcase_result_keyslist = sorted(testcase_result.keys(), key=lambda x: (x[0],x[1])) #排序
        for sheetn,testcase_id in testcase_result_keyslist:
            try:
                test_report_id = sheetn + '_' + str(testcase_id)
                testcase_name = TestCase.TestCaseXls.get_TestCaseName(sheetn, testcase_id)
                interface_type = TestCase.TestCaseXls.get_TestType(sheetn, testcase_id)
                interface_name = TestCase.TestCaseXls.get_TestItem(sheetn, testcase_id)

                testresult = self.testcase_result[(sheetn, testcase_id)][0]
                try:
                    testinfo = self.testcase_result[(sheetn, testcase_id)][1]
                except:
                    testinfo = ''

                if 'PASS' == testresult:
                    resultcolor = '#00ff00'
                elif 'FAIL' == testresult:
                    resultcolor = '#F9032C'
                else:
                    resultcolor = '#DA03C5'
                try:
                    tab << pyh.tr(pyh.td(test_report_id, align='left') + pyh.td(ch2s(testcase_name), align='left') +
                        pyh.td(ch2s(interface_name), align='left') + pyh.td(ch2s(interface_type), align='left') +
                        pyh.th(ch2s(testresult), bgcolor=resultcolor, align='left') + pyh.th(ch2s(testinfo), align='left'))

                except AttributeError as e:
                    tab << pyh.tr(pyh.td(test_report_id, align='left') + pyh.td('', align='left') +
                        pyh.td('', align='left') + pyh.td('', align='left') +
                        pyh.th(ch2s(testresult), bgcolor=resultcolor, align='left') + pyh.th(ch2s(testinfo), align='left'))

            except Exception as e:
                PrintLog('exception',e)
                continue

        self._setfilename()
        page.printOut(self.filename)
        PrintLog('debug', '生成测试结果报告: %s', self.filename)
        return self.filename
