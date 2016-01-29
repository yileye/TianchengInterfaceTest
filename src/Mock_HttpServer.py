#coding=utf8
#######################################################
#filename:Mock_HttpServer.py
#author:defias
#date:2016-1
#function: http server
#######################################################
from Global import *
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingTCPServer
import TestCase
import urllib
import json
import ModMock
import threading

class Custom_HTTPRequestHandler(BaseHTTPRequestHandler):
    def __init__(self, *args):
        self.ModMockO = ModMock.ModMock()
        BaseHTTPRequestHandler.__init__(self, *args)

    def do_POST(self):
        '''
        Handle post request
        '''
        try:
            PrintLog('debug', '[%s] got connection from %s', threading.currentThread().getName(), self.client_address)

            # 解析请求参数
            path_list = self.path.split('?')
            request_params = path_list[-1]
            request_path = path_list[0]

            PrintLog('debug', '[%s] get data! path: %s\nparams: %s ', threading.currentThread().getName(), request_path, request_params)
            data = self._getdata(request_path, request_params)
            PrintLog('debug', '[%s] write data! data: %s', threading.currentThread().getName(), data)
            self._writedata(data)

        except Exception as e:
            PrintLog('exception',e)

    def _getdata(self, request_path, request_params):
        '''
        Post response data
        '''
        request_params = urllib.unquote(request_params)
        if 'favicon.ico' == request_params:
            return None

        #从参数中解析出jsonString字典
        jsonString = request_params.split('&')[0]
        jsonStringvalues = jsonString.split('=')[-1]
        print 'jsonStringvalues:',jsonStringvalues
        jsonStringDict = json.loads(jsonStringvalues)

        if '/NiwoPassport/PostGetUserIdByMobile' == request_path:
            PrintLog('debug', '[%s] Interface: GetUserIdByMobile! jsonStringDict: %s ', threading.currentThread().getName(), jsonStringDict)
            return self._getdata_GetUserIdByMobile(jsonStringDict)
        elif '/UserMoney/PostUserStatistMoneyInfo' == request_path:
            PrintLog('debug', '[%s] Interface: UserStatistMoneyInfo! jsonStringDict: %s ', threading.currentThread().getName(), jsonStringDict)
            return self._getdata_UserStatistMoneyInfo(jsonStringDict)
        elif '/Common/PostUserInfoNew' == request_path:
            PrintLog('debug', '[%s] Interface: UserInfoNew! jsonStringDict: %s ', threading.currentThread().getName(), jsonStringDict)
            return self._getdata_UserInfoNew(jsonStringDict)
        else:
            return None

    def _getdata_GetUserIdByMobile(self, jsonStringDict):
        '''
        Interface: GetUserIdByMobile
        '''
        response = {}
        userMobile = jsonStringDict['userMobile']
        userid = userMobile     #将userMobile作为userid返回
        response['userId'] = userid
        response = json.dumps(response)
        PrintLog('debug', '[%s] Response Data: %s', threading.currentThread().getName(), response)
        return response

    def _getdata_UserStatistMoneyInfo(self, jsonStringDict):
        '''
        Interface: UserStatistMoneyInfo
        '''
        response = '{"FirstLoanDate":"","TotalLoanCount":0,"TotalLoanMoney":0,"DelayTotalCount":0,"DelayToalMoney":0,"WaitReturnMoney":0,\
        "FirstInvestDate":"","TotalInvestCount":0,"TotalInvestMoney":0,"RecentOneYearAvgInvestCount":0,"RecentOneYearAvgInvestMoney":0,\
        "RecentOneYearInvestCount":0,"RecentOneYearInvestMoney":0,"RecentOneYearAvgInvestDeadline":0,"DueinTotalMoney":0,"DueinTotalDay":0,\
        "ArgDueinMoney":0,"AviMoney":0,"DueinPlusAviMoney":0,"ReturnCode":1,"ReturnMessage":"成功","UserId":"3c90ae9a-d45e-447c-80af-3c2078ab5f48",\
        "UserName":"wal398139444","IDCardNo":"43052519861228611X","TuanDaiUserType":2}'
        response = json.loads(response)

        userid = jsonStringDict['UserId']
        userMobile = userid

        sheet, tid = self.ModMockO.getSheetId_from_UserMobile(userMobile)
        MockData = TestCase.TestCaseXls.get_MockData(sheet, tid)
        PrintLog('debug', '[%s] sheet: %s id: %s\nMockData: %s ', threading.currentThread().getName(), sheet, tid, MockData)
        MockData = self.ModMockO.parseMockData(MockData)
        if MockData is False:
            return None
        HTTPMockDate = MockData[0]

        RecentOneYearTotalLoanCount = HTTPMockDate["tuandai_loan_times"]
        RecentOneYearTotalLoanMoney = HTTPMockDate["tuandai_loan_menoy"]
        response['RecentOneYearTotalLoanCount'] = RecentOneYearTotalLoanCount
        response['RecentOneYearTotalLoanMoney'] = RecentOneYearTotalLoanMoney
        response = json.dumps(response)
        PrintLog('debug', '[%s] Response Data: %s', threading.currentThread().getName(), response)
        return response

    def _getdata_UserInfoNew(self, jsonStringDict):
        '''
        Interface: UserInfoNew
        '''
        response = '{"accountAmount":0,"recoverBorrowOut":0,"recoverDueOutPAndI":0,"status":"00","desc":""}'
        response = json.loads(response)

        userid = jsonStringDict['UserId']
        userMobile = userid

        sheet, tid = self.ModMockO.getSheetId_from_UserMobile(userMobile)
        MockData = TestCase.TestCaseXls.get_MockData(sheet, tid)
        PrintLog('debug', '[%s] sheet: %s id: %s\nMockData: %s ', threading.currentThread().getName(), sheet, tid, MockData)
        MockData = self.ModMockO.parseMockData(MockData)
        if MockData is False:
            return None
        HTTPMockDate = MockData[0]

        AvgDayDueInMoneyOneYear = HTTPMockDate["tuandai_amount"]
        response['AvgDayDueInMoneyOneYear'] = AvgDayDueInMoneyOneYear
        response = json.dumps(response)
        PrintLog('debug', '[%s] Response Data: %s', threading.currentThread().getName(), response)
        return response


    def _writedata(self, data):
        '''Write header'''
        if data is not None:
            self.send_response(200)
            self.send_header('Content-Type','text/plain;charset=utf-8')
            self.end_headers()
            self.wfile.write(data)
        else:
            self.send_response(404)
            self.send_header('Content-Type','text/plain;charset=utf-8')
            self.end_headers()
            self.wfile.write('None')

"""
class Custom_HTTPServer(HTTPServer):
    '''
    自定义HTTPServer
    '''
    def serve_forever(self):
        '''
        serve forever
        '''
        self.stopped = False
        while not self.stopped:
            self.handle_request()

    def stop_server(self, host, port):
        '''
        stop server
        '''
        self.stopped = True
        str_address = str(host)+':'+str(port)
        conn = httplib.HTTPConnection(str_address)
        conn.request("QUIT", "/")

"""

class HttpServer(object):
    '''
    Mock HttpServer
    '''
    def __init__(self):
        ModMockO = ModMock.ModMock()
        HTTPinfo = ModMockO.getRuncaseEnvironment_HTTP()
        self.host, self.port = HTTPinfo
        self.httpd_address = (self.host, self.port)

    def Start(self):
        '''
        启动
        '''
        try:
            self.Custom_httpd = HTTPServer(self.httpd_address, Custom_HTTPRequestHandler)
            #self.Custom_httpd = ThreadingTCPServer(self.httpd_address, Custom_HTTPRequestHandler)
            PrintLog('debug', '[%s] Http Server is Start Running %s:%s...', threading.currentThread().getName(), self.host, self.port)
            self.Custom_httpd.serve_forever()

        except KeyboardInterrupt as e:
            PrintLog('exception',e)
            self.Custom_httpd.shutdown
        except Exception as e:
            PrintLog('exception',e)

