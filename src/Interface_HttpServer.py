#coding=utf8
#######################################################
#filename:Interface_HttpServer.py
#author:defias
#date:2016-1
#function: http server
#######################################################
from Global import *
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingTCPServer
import urllib
import json
import re
import threading

class HttpServer(object):
    '''
    Http服务
    '''
    def __init__(self,HTTPMockData, HTTPinfo):
        self.HTTPMockData = HTTPMockData
        self.HTTPinfo = HTTPinfo
        HTTPhost, HTTPport = self.HTTPinfo
        httpd_address = (HTTPhost, HTTPport)
        self.myhttpd = ThreadingTCPServer(httpd_address, self.BuilderHandle())

    def Start(self):
        '''
        启动
        '''
        PrintLog('debug', '[%s] http server is running....', threading.currentThread().getName())
        self.myhttpd.serve_forever()

    def BuilderHandle(self):
        '''
        构建Handle类
        '''
        HTTPMockData = self.HTTPMockData
        class Custom_HTTPRequestHandler(BaseHTTPRequestHandler):
            '''
            Handle
            '''
            def do_POST(self):
                '''
                post request
                '''
                PrintLog('debug', '[%s] got connection from:client_address:%s', threading.currentThread().getName(), self.client_address)
                #解析请求参数
                path_list = self.path.split('?')
                request_params = path_list[-1]
                request_path = path_list[0]

                data = self._getdata(request_path, request_params)
                PrintLog('debug', '[%s] get data: %s', threading.currentThread().getName(), data)

                self._writedata(data)
                PrintLog('debug', '[%s] write data', threading.currentThread().getName())

            def _getdata(self, path, params):
                '''Post response data'''
                PrintLog('debug', '[%s] request path: %s  request params: %s', threading.currentThread().getName(), path, params)
                params = urllib.unquote(params)
                if 'favicon.ico' == params:
                    post_interface = 'None'
                elif '/NiwoPassport/PostGetUserIdByMobile' == path:
                    post_interface = 'GetUserIdByMobile'
                elif '/UserMoney/PostUserStatistMoneyInfo' == path:
                    post_interface = 'UserStatistMoneyInfo'
                elif '/Common/PostUserInfoNew' == path:
                    post_interface = 'UserInfoNew'
                else:
                    post_interface = 'None'

                PrintLog('debug', '[%s] post_interface: %s', threading.currentThread().getName(), post_interface)
                if post_interface not in ['GetUserIdByMobile','UserStatistMoneyInfo','UserInfoNew']:
                    return None
                jsonString = params.split('&')[0]
                jsonStringvalues = jsonString.split('=')[-1]
                jsonStringlist = json.loads(jsonStringvalues)

                #解析用例数据HTTPMockData
                tuandai_loan_times = HTTPMockData['tuandai_loan_times']
                tuandai_loan_menoy = HTTPMockData['tuandai_loan_menoy']
                tuandai_amount = HTTPMockData['tuandai_amount']
                PrintLog('debug', '[%s] Read HTTPMockData: tuandai_loan_times: %s tuandai_loan_menoy: %s tuandai_amount: %s', threading.currentThread().getName(), tuandai_loan_times, tuandai_loan_menoy, tuandai_amount)

                #GetUserIdByMobile
                if post_interface == 'GetUserIdByMobile':
                    response_list = {}
                    userMobile = jsonStringlist['userMobile']
                    userid = 'testing'     #testing
                    response_list['userId'] = userid
                    response_jsonstr =  json.dumps(response_list)

                #UserStatistMoneyInfo
                elif post_interface == 'UserStatistMoneyInfo':
                    response_jsonstr = '{"FirstLoanDate":"","TotalLoanCount":0,"TotalLoanMoney":0,"DelayTotalCount":0,"DelayToalMoney":0,"WaitReturnMoney":0,"FirstInvestDate":"","TotalInvestCount":0,"TotalInvestMoney":0,"RecentOneYearAvgInvestCount":0,"RecentOneYearAvgInvestMoney":0,"RecentOneYearInvestCount":0,"RecentOneYearInvestMoney":0,"RecentOneYearAvgInvestDeadline":0,"DueinTotalMoney":0,"DueinTotalDay":0,"ArgDueinMoney":0,"AviMoney":0,"DueinPlusAviMoney":0,"ReturnCode":1,"ReturnMessage":"成功","UserId":"3c90ae9a-d45e-447c-80af-3c2078ab5f48","UserName":"wal398139444","IDCardNo":"43052519861228611X","TuanDaiUserType":2}'
                    response_dic = json.loads(response_jsonstr)
                    #userid = jsonStringlist['UserId']
                    #assert userid == 'testing'

                    response_dic['RecentOneYearTotalLoanCount'] = tuandai_loan_times
                    response_dic['RecentOneYearTotalLoanMoney'] = tuandai_loan_menoy
                    response_jsonstr = json.dumps(response_dic)

                #UserInfoNew
                elif post_interface == 'UserInfoNew':
                    response_jsonstr = '{"accountAmount":0,"recoverBorrowOut":0,"recoverDueOutPAndI":0,"status":"00","desc":""}'
                    response_dic = json.loads(response_jsonstr)
                    #userid = jsonStringlist['UserId']
                    #assert userid == 'testing'

                    response_dic['AvgDayDueInMoneyOneYear'] = tuandai_amount
                    response_jsonstr = json.dumps(response_dic)

                else:
                    return None
                return response_jsonstr

            def _writedata(self, data):
                '''Write header'''
                if data is None:
                    self.send_response(404)
                    self.send_header('Content-Type','text/plain;charset=utf-8')
                    self.end_headers()
                    self.wfile.write('None')
                else:
                    self.send_response(200)
                    self.send_header('Content-Type','text/plain;charset=utf-8')
                    self.end_headers()
                    self.wfile.write(data)
