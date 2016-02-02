#coding=utf8
#######################################################
#filename:MockHttpServer.py
#author:defias
#date:2016-1
#function: http server
#######################################################
from Global import *
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
#from SocketServer import ThreadingTCPServer
import MockData
import urllib
import json
import ModMock

class Custom_HTTPRequestHandler(BaseHTTPRequestHandler):
    def __init__(self, *args):
        self.ModMockO = ModMock.ModMock()
        BaseHTTPRequestHandler.__init__(self, *args)

    def do_POST(self):
        '''
        Handle post request
        '''
        try:
            PrintLog('debug', '[HttpServer] got connection from %s',  self.client_address)

            # 解析请求参数
            path_list = self.path.split('?')
            request_params = path_list[-1]
            request_path = path_list[0]

            PrintLog('debug', '[HttpServer] get data! path: %s\nparams: %s ',  request_path, request_params)
            data = self._getdata(request_path, request_params)
            PrintLog('debug', '[HttpServer] write data! data: %s',  data)
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
        jsonStringDict = json.loads(jsonStringvalues)

        if '/NiwoPassport/PostGetUserIdByMobile' == request_path:
            PrintLog('debug', '[HttpServer] Interface: GetUserIdByMobile!\njsonStringDict: %s ',  jsonStringDict)
            return self._getdata_GetUserIdByMobile(jsonStringDict)
        elif '/UserMoney/PostUserStatistMoneyInfo' == request_path:
            PrintLog('debug', '[HttpServer] Interface: UserStatistMoneyInfo!\njsonStringDict: %s ',  jsonStringDict)
            return self._getdata_UserStatistMoneyInfo(jsonStringDict)
        elif '/Common/PostUserInfoNew' == request_path:
            PrintLog('debug', '[HttpServer] Interface: UserInfoNew!\njsonStringDict: %s ',  jsonStringDict)
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
        PrintLog('debug', '[HttpServer] Response Data: %s',  response)
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

        ID = self.ModMockO.HttpData_Key2ID(userMobile)
        HTTPMockDate = MockData.MockDataXls.get_MockData(ID)
        PrintLog('debug', '[HttpServer] ID: %s\nHTTPMockDate: %s ', ID, HTTPMockDate)
        HTTPMockDate = self.ModMockO.parseMockData(HTTPMockDate)
        if HTTPMockDate is False:
            return None

        RecentOneYearTotalLoanCount = HTTPMockDate["tuandai_loan_times"]
        RecentOneYearTotalLoanMoney = HTTPMockDate["tuandai_loan_menoy"]
        response['RecentOneYearTotalLoanCount'] = RecentOneYearTotalLoanCount
        response['RecentOneYearTotalLoanMoney'] = RecentOneYearTotalLoanMoney
        response = json.dumps(response)
        PrintLog('debug', '[HttpServer] Response Data: %s',  response)
        return response

    def _getdata_UserInfoNew(self, jsonStringDict):
        '''
        Interface: UserInfoNew
        '''
        response = '{"accountAmount":0,"recoverBorrowOut":0,"recoverDueOutPAndI":0,"status":"00","desc":""}'
        response = json.loads(response)

        userid = jsonStringDict['UserId']
        userMobile = userid

        ID = self.ModMockO.HttpData_Key2ID(userMobile)
        HTTPMockDate = MockData.MockDataXls.get_MockData(ID)
        PrintLog('debug', '[HttpServer] ID: %s\nHTTPMockDate: %s ', ID, HTTPMockDate)
        HTTPMockDate = self.ModMockO.parseMockData(HTTPMockDate)
        if HTTPMockDate is False:
            return None

        AvgDayDueInMoneyOneYear = HTTPMockDate["tuandai_amount"]
        response['AvgDayDueInMoneyOneYear'] = AvgDayDueInMoneyOneYear
        response = json.dumps(response)
        PrintLog('debug', '[HttpServer] Response Data: %s',  response)
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

    def run(self):
        '''
        启动
        '''
        try:
            self.Custom_httpd = HTTPServer(self.httpd_address, Custom_HTTPRequestHandler)
            PrintLog('debug', '[HttpServer] Http Server is Start Running %s:%s...',  self.host, self.port)
            self.Custom_httpd.serve_forever()
        except KeyboardInterrupt as e:
            PrintLog('exception',e)
            self.Custom_httpd.shutdown
        except Exception as e:
            PrintLog('exception',e)
