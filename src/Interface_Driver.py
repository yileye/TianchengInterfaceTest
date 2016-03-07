#coding=utf8
#######################################################
#filename:Interface_Driver.py
#author:defias
#date:2015-8
#function:天秤测试驱动类
#######################################################
from Global import *
import requests
import MySQLdb
import threading

class Interface_Http(object):
    '''
    HTTP接口
    '''
    def __init__(self, url):
        '''
        初始化
        '''
        self.url = url

    def get(self):
        '''
        HTTP GET方法
        '''
        try:
            return requests.get(self.url, timeout=5)
        except Exception as e:
            PrintLog('exception',e)
            return False

    def post(self, headers, params):
        '''
        HTTP POST方法
        '''
        try:
            if type(params) is unicode:
                PrintLog('info', '[%s] params encode to utf-8', threading.currentThread().getName())
                params = params.encode('utf-8')   #对unicode编码为utf8后再发送，确保无中文编码问题
            #PrintLog('debug', '[%s] url: %s data: %s headers: %s  type(data): %s', threading.currentThread().getName(), self.url, params, headers, type(params))
            return requests.post(self.url, data=params, headers=headers, timeout=5)
        except Exception as e:
            PrintLog('exception',e)
            return False


class Interface_DoData(object):
    '''
    Mysql数据处理接口
    '''
    def __init__(self, dbinfo):
        '''
        初始化-连接数据库
        '''
        host, port, username, passwd, dbname = dbinfo
        PrintLog('info', '[%s] connecting mysql db: %s %s:%s %s/%s', threading.currentThread().getName(), dbname, host, port, username, passwd)
        self.conn = MySQLdb.connect(host=host,user=username,passwd=passwd,port=port,charset='utf8')  #连接数据库
        self.conn.select_db(dbname)  #选择数据库
        self.cur = self.conn.cursor()


    def __del__(self):
        '''
        释放数据库连接
        '''
        PrintLog('info', '[%s] closing mysql db connection', threading.currentThread().getName())
        self.cur.close()
        self.conn.close()


    def getTableMaxid(self, tablelist):
        '''
        获取table-maxid键值对字典
        '''
        TableMaxid = {}
        for tablen in tablelist:
            query_str = "SELECT MAX(id) FROM " + tablen
            self.cur.execute(query_str)
            self.conn.commit()
            maxid = self.cur.fetchone()[0]
            TableMaxid[tablen] = maxid
        return TableMaxid

    def _insert(self, insert_datalist):
        '''
        向表中插入数据 [(table, fields, values), ...]
        '''
        PrintLog('debug', '[%s] 向表中插入数据: 参数:%s', threading.currentThread().getName(), insert_datalist)
        for i in xrange(len(insert_datalist)):
            table = insert_datalist[i][0]

            #插数据
            query_insert = 'INSERT INTO ' + table + '('
            query_fields = 'VALUES('
            query_value = []
            for field in insert_datalist[i][1]:
                query_insert = query_insert + field + ','
                query_fields = query_fields + '%s' + ','
            for value in insert_datalist[i][2]:
                query_value.append(value)
            try:
                if not query_value:
                    raise ValueError
                query_str =  query_insert[:-1] + ') '  + query_fields[:-1] + ')'
                PrintLog('debug', '[%s] 执行插入SQL: query_str: %s  query_value: %s', threading.currentThread().getName(), query_str, tuple(query_value))
                self.cur.execute(query_str, tuple(query_value))
                self.conn.commit()
            except Exception as e:
                PrintLog('exception',e)
                return False
        return True

    def insert(self, insert_datalist, *function):
        '''
        向表中插入数据
        '''
        if function:
            PrintLog('debug', '[%s] 调用回调: 参数:%s', threading.currentThread().getName(), insert_datalist)
            cbresult = function[0](insert_datalist)
            PrintLog('info', '[%s] 回调结果:%s', threading.currentThread().getName(), cbresult)
            insert_datalist = cbresult[0]
            userid = cbresult[1]
        if self._insert(insert_datalist):
            if 'userid' in locals().keys():
                return userid
            else:
                return True
        else:
            return False
