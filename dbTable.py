from wx import grid

class EmptyTable(grid.PyGridTableBase):
    def __init__(self):
        grid.PyGridTableBase.__init__(self)

class DBTable(grid.PyGridTableBase):
    """Class to wrap a database table that can be assigned to a grid
    
    Inspired by wxPyDBAPITable by Nathan R Yergler

    Changed by Ioan Coman on March 7, 2017
    """
    def __init__(self, db, tableName):
        grid.PyGridTableBase.__init__(self)
        self.__db=db
        self.tableName=tableName
        self.__rows = []
        self.getData(tableName)

    def getData(self, tableName):
        self.tableName=tableName
        self.__rows=self.__db.getRows(tableName)
        self._rowCount=len(self.__rows)
        self._colNames=[col[0] for col in self.__db.getColumns(tableName)]
        self._colCount=len(self._colNames)

    # Table level methods
    def GetNumberRows(self):
        return self._rowCount

    def GetNumberCols(self):
        return self._colCount

    def AppendRows(self, numRows=1):
        # Implement this when we want to modify data
        # Should just be a simple insert (?)
        #print "AppendRows:",numRows
        return True

    # Cell level values
    def IsEmptyCell(self, row, col):
        if self.__rows[row][col] == "" or self.__rows[row][col] is None:
            return True
        else:
            return False

    def GetValue(self, row, col):
        return self.__rows[row][col]

    def SetValue(self, row, col, valstr):
        recid = self.__rows[row][0]
        self.__rows[row][col] = self.__db.SetValue(self.tableName, recid, col, valstr)
        return True

    def NewValue(self):
        recid = None
        self.__db.SetValue(self.tableName, recid, None, None)
        return True

    def DeleteValues(self, recordlist):
        for recid in recordlist:
            #on column 0 is the primary key
            pk = self.__rows[recid][0]
            self.__db.DeleteValue(self.tableName, pk)



    # Label methods
    def GetRowLabelValue(self, row):
        # A record number will do fine, thanks
        #return 'row{}'.format(row+1)
        return row+1

    def GetColLabelValue(self, col):
        return self._colNames[col]

    def SetRowLabelValue(self, row, label):
        # Disable this for now
        #print "DBTable SetRowLabelValue",row, label
        pass

    def SetColLabelValue(self, row, label):
        # Disable this for now
        #print "DBTable SetColLabelValue:",row,label
        pass

    # Miscellaneous methods
    def refresh(self):
        #print "refresh"
        #if self.__stmt:
        #    self.getData(self.__stmt)
        pass

    def GetRowLabelList(self):
        # Not today thank you
        pass

    def GetColLabelList(self):
        return self._colNames
