# SQL Table Editor

A small application written in [Python 2.7](https://www.python.org/) with [SQLAlchemy](http://www.sqlalchemy.org/), [PythonCard](http://pythoncard.sourceforge.net/) and [wxGrid](https://wiki.wxpython.org/wxGrid) - [blog announcement](http://rainbowheart.ro/548).

![SQL Table Editor - edit blog gategories](http://rainbowheart.ro/static/uploads/1/2017/5/sqltableeditor.jpg)

The python program require config.ini file created like that:

```ini

#
# Config for SQL Table Editor
#

title = SQL Table Editor

DSN = mssql+pymssql://user:password@localhost/wmsfd
DSN = mssql+pymssql://user:password@localhost/magazie
DSN = postgresql://ioan:***@localhost/blog
DSN = postgresql://ioan:***@localhost/nopass
DSN = mysql+pymysql://root:admin@localhost/database1
DSN = sqlite+pysqlite:///python.db

```

No copyright specified.

Feel free to use this software for both personal and commercial.
