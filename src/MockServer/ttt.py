 def StartMock(self, MockData, ModO, TestEnvironment):
        '''
        开启Mock线程
        '''
        if MockData != '':
            PrintLog('debug', '[%s] 启动MOCK服务子线程: MockData: %s\nTestEnvironment: %s', threading.currentThread().getName(), MockData, TestEnvironment)
            StartResult = Interface_Mock.StartMockServer(MockData, ModO, TestEnvironment)
            PrintLog('debug', '[%s] 启动MOCK服务子线程完成: StartResult: %s', threading.currentThread().getName(), StartResult)
            if StartResult is False:
                PrintLog('debug', '[%s] 启动MOCK服务子线程时出现异常', threading.currentThread().getName())
                return False

            #确保Mock子线程服务开启
            if 'TABLE' in StartResult:
                while not Global.isTABLE:
                    PrintLog('debug', '[%s] sleep isTABLE...', threading.currentThread().getName())
                    time.sleep(0.5)
                PrintLog('debug', '[%s] sleep isTABLE end', threading.currentThread().getName())

                if Global.isTABLE == 'except':
                    PrintLog('debug', '[%s] TABLEThread线程异常', threading.currentThread().getName())
                    return False
                elif Global.isTABLE is True:
                    Global.isTABLE = False
                    PrintLog('debug', '[%s] TABLEThread线程服务完成', threading.currentThread().getName())

            if 'MQMOCK' in StartResult:
                while not Global.isMQMock:
                    PrintLog('debug', '[%s] sleep isMQMock...', threading.currentThread().getName())
                    time.sleep(0.5)
                PrintLog('debug', '[%s] sleep isMQMock end', threading.currentThread().getName())

                if Global.isMQMock == 'except':
                    PrintLog('debug', '[%s] MQMockThread线程异常', threading.currentThread().getName())
                    return False
                elif Global.isMQMock is True:
                    Global.isMQMock = False
                    PrintLog('debug', '[%s] MQMockThread线程服务开启', threading.currentThread().getName())

            if 'HTTPMOCK' in StartResult:
                while not Global.isHTTPMock:
                    PrintLog('debug', '[%s] sleep isHTTPMock...', threading.currentThread().getName())
                    time.sleep(0.5)
                PrintLog('debug', '[%s] sleep isHTTPMock end', threading.currentThread().getName())

                if Global.isHTTPMock == 'except':
                    PrintLog('debug', '[%s] HTTPMockThread线程异常', threading.currentThread().getName())
                    return False
                elif Global.isHTTPMock is True:
                    Global.isHTTPMock = False
                    PrintLog('debug', '[%s] HTTPMockThread线程服务开启', threading.currentThread().getName())
            time.sleep(10)
            return StartResult

    def EndMock(self, MockData, StartResult):
        '''
        结束Mock线程
        '''
        if MockData != '' and StartResult != {} and StartResult != False:
            PrintLog('debug', '[%s] EndMock sleep...', threading.currentThread().getName())
            time.sleep(5)   #延时一段时间，测试操作成功后，不代表第三方服务就可以结束，这里通过延时一固定时间提供第三方服务，并不是非常可靠的做法
            PrintLog('debug', '[%s] 结束MOCK服务子线程， StartResult: %s', threading.currentThread().getName(), StartResult)
            if 'HTTPMOCK' in StartResult:
                HTTPMockThreadO = StartResult['HTTPMOCK']
                try:
                    HTTPMockThreadO.myhttpd.stop_server()
                except:
                    pass
                    PrintLog('debug', '[%s]  HTTPMockThreadO.myhttpd.stop_server() end', threading.currentThread().getName())
                while HTTPMockThreadO.isAlive():
                    time.sleep(1)
                PrintLog('debug', '[%s] HTTPMockThreadO线程服务结束', threading.currentThread().getName())

            if 'MQMOCK' in StartResult:
                MQMockThreadO = StartResult['MQMOCK']
                try:
                    MQMockThreadO.connection.close()
                except:
                    pass
                    PrintLog('debug', '[%s]  MQMockThreadO.connection.close() end', threading.currentThread().getName())
                while MQMockThreadO.isAlive():
                    time.sleep(1)
                PrintLog('debug', '[%s] MQMockThreadO线程服务结束', threading.currentThread().getName())

            if 'TABLE' in StartResult:
                TABLEThreadO = StartResult['TABLE']
                if TABLEThreadO.isAlive():
                    TABLEThreadO.join()
                PrintLog('debug', '[%s] TABLEThreadO线程服务结束', threading.currentThread().getName())










    def parseMockDataForDriver(self, MockData):
        '''
        解析MockData
        '''
        try:
            if MockData == '':
                raise ValueError
            else:
                MockDataDict = json.loads(MockData)
            return MockDataDict
        except Exception as e:
            PrintLog('exception',e)
            return False
