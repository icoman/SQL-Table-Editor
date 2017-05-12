#!/usr/bin/python

"""
Module Name: genericSqlalchemy
Description: Plug in for PythonCard application dbBrowse
to provide SQL Alchemy specific functionality

Author: Ioan Coman, March 7, 2017

All SQL table should have a primary key.
If not, then sqlalchemy.exc.ArgumentError:
Mapper could not assemble any primary key columns for mapped table



"""
__version__="0.1"
__date__="7 March, 2017"
__author__="Ioan Coman"


from sqlalchemy import text, create_engine, MetaData, Table, Column, BigInteger, ForeignKey, inspect
from sqlalchemy.orm import mapper, clear_mappers, sessionmaker, relationship
from sqlalchemy.sql import default_comparator


#mapped table
class myTable(object):
    pass




class browse:

    # Connection is DSN
    def __init__(self, DSN):
        "Setup the database connection"
        self.engine = create_engine(DSN)
        self.engine.echo = False
        self.metadata = MetaData(self.engine)
        self._tableName = ''

    def _getTableFields(self, tableName):
        '''
        used by getColumns and getRows
        build table header in a sorted order with primary key first (pk on column 0)
        '''
        if not tableName:
            raise Exception('tableName is None')
        if tableName != self._tableName:
            self._tableName = tableName
            clear_mappers()
            mapper(myTable, Table(self._tableName, self.metadata, autoload=True))
            insp = inspect(myTable)
            self._pk_name = None
            self._fields = []
            L = insp.all_orm_descriptors.keys()
            L.sort()
            for columnName in L:
                field = myTable.__getattribute__(myTable, columnName)
                if field.primary_key:
                    self._pk_name = columnName
                else:
                    self._fields.append(columnName)
            if self._pk_name:
                #put primary key first in list
                self._fields = [self._pk_name] + self._fields

    def getTables(self):
        "Return a list of all tables"
        self.metadata.reflect(self.engine)
        return self.metadata.tables.keys()

    def getColumns(self, tableName):
        "Get the definition of the columns in tableName"
        self._getTableFields(tableName)
        columnDefs = []
        for columnName in self._fields:
            field = myTable.__getattribute__(myTable,columnName)
            dataType = ''
            precision = 0
            nullable = False
            primary_key = field.primary_key
            default = ''
            columnDefs.append((columnName, dataType, precision, nullable, primary_key, default))
        return columnDefs

    def getRows(self, tableName):
        "Get all of the rows from tableName"
        self._getTableFields(tableName)
        Session = sessionmaker(bind=self.engine)
        session = Session()
        pkfield = myTable.__getattribute__(myTable, self._pk_name)
        ret = []
        try:
            if self.filter:
                q = session.query(myTable).order_by(pkfield.asc()).filter(text(self.filter)).limit(1000).all()
            else:
                q = session.query(myTable).order_by(pkfield.asc()).limit(1000).all()
            for row in q:
                l = []
                for i in self._fields:
                    value = row.__getattribute__(i)
                    l.append(value)
                ret.append(l)
        except:
            pass
        session.close()
        return ret

    def SetValue(self, tableName, recid, col, valstr):
        ret = valstr
        Session = sessionmaker(bind=self.engine)
        session = Session()
        try:
            self._getTableFields(tableName)
            pkfield = myTable.__getattribute__(myTable, self._pk_name)
            if recid:
                #print "genericSqlalchemy SetValue {} = {} WHERE ID = {}".format(self._fields[col],valstr,recid)
                ob = session.query(myTable).filter(pkfield == recid).one()
                ob.__setattr__(self._fields[col], valstr)
            else:
                ob = myTable()
                session.add(ob)
                ret = 'new'
            session.commit()
        except Exception as ex:
            print ex
            ret = str(ex)[:50]
        session.close()
        return ret

    def DeleteValue(self, tableName, recid):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        try:
            self._getTableFields(tableName)
            pkfield = myTable.__getattribute__(myTable, self._pk_name)
            #print "genericSqlalchemy DeleteValue DELETE FROM {} WHERE ID = {}".format(tableName,recid)
            ob = session.query(myTable).filter(pkfield == recid).one()
            session.delete(ob)
            session.commit()
        except Exception as ex:
            print ex
        session.close()
        return
