#coding=utf-8
#######################################################
#filename:ExcelRW.py
#author:defias
#date:2015-4-27
#function:read or write excel file test
#######################################################
import xlrd
import xlutils.copy

class XlsEngine():
    """
    The XlsEngine is a class for excel operation
    """
    def __init__(self,xlsname):
        """
        define class variable
        """
        self.xlsname = xlsname
        self.xlrd_object = xlrd.open_workbook(self.xlsname)

    def getsheets(self):
        """
        get xls file's sheets
        """
        return self.xlrd_object.sheet_names()


    def getrows(self,sheetname):
        """
        get xls file all rows
        """
        worksheet = self.xlrd_object.sheet_by_name(sheetname)
        return worksheet.nrows


    def getcols(self,sheetname):
        """
        get xls file all cols
        """
        worksheet = self.xlrd_object.sheet_by_name(sheetname)
        return worksheet.ncols


    def readrow(self,sheetname,rown):
        """
        read file's a row content to list
        """
        worksheet = self.xlrd_object.sheet_by_name(sheetname)
        return worksheet.row_values(rown)


    def readcol(self,sheetname,coln):
        """
        read file's a col content to list
        """
        worksheet = self.xlrd_object.sheet_by_name(sheetname)
        return worksheet.col_values(coln)


    def readcell(self,sheetname,rown,coln):
        """
        read file's cell
        """
        worksheet = self.xlrd_object.sheet_by_name(sheetname)
        return worksheet.cell_value(rown,coln)


    def writecell(self,sheetn,rown,coln,value):
        """
        write a cell to file,other cell is not change
        """
        pass
