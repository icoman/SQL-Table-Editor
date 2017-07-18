#!/usr/bin/python

"""
    Generic SQL Table Editor
    March 7, 2017

"""

import os, string, sys
from PythonCard import model, dialog
import wx

from dbTable import EmptyTable, DBTable
import genericSqlalchemy



def getPropsDict(filename, sep = '=', comment = ";#"):
    '''
    Read config file and return a dict key:value
    If a key is defined multiple times, value is converted to a list

    Arguments:
    filename = config file name
    sep = key-value separator
    comment = a list of chars which define start of comments
    
    '''
    ret = {}
    f = open(filename,"rt")
    accumulator = ''
    flag = False
    while True:
        line = f.readline()
        if not line:
            #line must have at least \r\n
            break
        line = line.replace('\r', '')
        line = line.replace('\n', '')
        line = line.lstrip()
        if not line:
            #line is empty
            continue
        if line[0] in comment:
            #ignore line because
            #the line starts with a comment
            continue
        if line[-1] == '\\':
            #data continue on next line
            line = line[:-1]
            if flag:
                accumulator = string.join((accumulator, line), ' ')
            else:
                accumulator = line
            flag = True
            continue
        if flag:
            accumulator = string.join((accumulator, line), ' ')
            line = accumulator
            accumulator = ''
            flag = False
        #split line
        ix = line.find(sep)
        if ix > 0:
            key = line[:ix].rstrip()
            value = line[ix+1:].lstrip().rstrip()
            if ret.has_key(key):
                old = ret[key]
                if type(old) == type([]):
                    ret[key].append(value)
                else:
                    ret[key] = [old, value]
            else:
                ret[key] = value
    f.close()
    return ret




class MyBackground(model.Background):

    def on_close(self,evt):
        self.MakeModal(False)
        self.Destroy()

    def on_about_command(self, event):
        from PythonCard import __version__ as ver
        result = dialog.messageDialog(self, '''Generic SQL Editor

(C) 2017 Ioan Coman
http://rainbowheart.ro/

PythonCard version: {}
wx version: {}

Python version:
{}

'''.format(ver.VERSION_STRING, wx.version(), sys.version), 'About', wx.ICON_INFORMATION | wx.OK) #wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL)

    def on_initialize(self, event):
        #init
        if getattr(sys, 'frozen', False):
            self.DATAFOLDER = string.join((os.getcwd(),'..'),os.sep)
        else:
            self.DATAFOLDER = os.getcwd()
        configFilename = string.join((self.DATAFOLDER, "config.ini"), os.sep)
        self.config = getPropsDict(configFilename, '=') #sep is '='
        self.components.title.text = self.config.get('title','SQL Table Editor')
        self.title = self.components.title.text
        self.components.tableList.items = []
        self.components.tableList.enabled = False
        self.components.appendRecord.enabled = False
        self.components.deleteRecord.enabled = False
        self.components.Refresh.enabled = False
        self.components.filter.text = ''
        self.components.filter.enabled = False
        DSN = self.config.get('DSN',[])
        if type(DSN) == type([]):
            self.components.DSNList.items = DSN
        else:
            self.components.DSNList.items = [DSN]
            self.components.DSNList.selection = 0
            self.components.DSNList.stringSelection = DSN
            self.on_DSNList_select(None)
        accesspassword = self.config.get('accesspassword',None)
        accessprompt = self.config.get('accessprompt','Access Password:')
        if self.config.get('enabledelete', False):
            self.enabledelete = True
        else:
            self.enabledelete = False
        if accesspassword:
            result = dialog.passwordTextEntryDialog(self, 
                            accessprompt,
                            accessprompt,
                            '')
            if accesspassword == result.text:
                dialog.messageDialog(self, '''Ok!''', accessprompt,wx.ICON_INFORMATION | wx.OK) #wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL)
            else:
                sys.exit(1)


    def on_DSNList_select(self, event):
        #1 - select DSN
        DSN = self.components.DSNList.stringSelection
        if DSN:
            try:
                self.components.tableList.enabled = True
                self.components.appendRecord.enabled = False
                self.components.deleteRecord.enabled = False
                self.components.Refresh.enabled = False
                dbClass = genericSqlalchemy.browse
                self.db = dbClass(DSN)
                self.components.tableList.items = self.db.getTables()
                self.components.myGrid.SetTable(EmptyTable())
                self.components.myGrid.AutoSizeColumns()
                self.components.myGrid.AdjustScrollbars()
            except Exception as ex:
                dialog.messageDialog(self, str(ex), 'Error',wx.ICON_ERROR | wx.OK)

    def on_tableList_select(self, evt):
        #2 - select table
        table = self.components.tableList.stringSelection
        if table:
            try:
                self.db.filter = self.components.filter.text
                self.dbTable=DBTable(self.db, table)
                self.components.myGrid.SetTable(self.dbTable)
                self.components.myGrid.AutoSizeColumns()
                self.components.myGrid.AdjustScrollbars()
                self.components.filter.enabled = True
                self.components.appendRecord.enabled = True
                self.components.deleteRecord.enabled = self.enabledelete
                self.components.Refresh.enabled = True
            except Exception as ex:
                self.components.myGrid.SetTable(EmptyTable())
                self.components.myGrid.AutoSizeColumns()
                self.components.myGrid.AdjustScrollbars()
                dialog.messageDialog(self, str(ex), 'Error',wx.ICON_ERROR | wx.OK)

    def on_filter_textUpdate(self, evt):
        #3 - apply filter
        self.on_tableList_select(None)

    def on_refresh_command(self, evt):
        self.on_tableList_select(None)

    def on_addrec_command(self, evt):
        self.dbTable.NewValue()
        self.on_tableList_select(None)

    def on_delrec_command(self, evt):
        recordlist = self.components.myGrid.GetSelectedRows()
        if recordlist:
            message = 'Delete records:\n{} ?'.format(recordlist)
            result = dialog.messageDialog(self, message, 'Delete',wx.ICON_INFORMATION | wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL)
            if result.accepted:
                self.dbTable.DeleteValues(recordlist)
                self.on_tableList_select(None)
        else:
            dialog.messageDialog(self, 'Nothing selected.', 'Info',wx.ICON_INFORMATION | wx.OK)


def fix_frozen_apps():
    #
    #fix import for py2exe, cx_freeze, pyinstaller, ...
    #
    #import here whatever fail to import when application is frozen
    #
    import pyodbc, pymssql, _mssql
    from sqlalchemy.sql import default_comparator
    #from PythonCard.components import slider
    #from PythonCard.components import radiogroup
    from PythonCard.components import button
    #from PythonCard.components import list
    from PythonCard.components import choice
    from PythonCard.components import statictext
    #from PythonCard.components import checkbox
    #from PythonCard.components import gauge
    #from PythonCard.components import multicolumnlist
    #from PythonCard.components import passwordfield
    from PythonCard.components import textarea
    from PythonCard.components import combobox
    #from PythonCard.components import calendar
    from PythonCard.components import grid


if __name__ == '__main__':
    app = model.Application(MyBackground)
    app.MainLoop()
