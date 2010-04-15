import sqlite3
from sqlite3 import Error

from humble.database import DatabaseInterface

class Sqlite( DatabaseInterface ):

    def __init__(self, file ):
        # Open up the sqlite file
        self.connection = sqlite3.connect( file )
        # Grab our cursor
        self.cursor = self.connection.cursor()

    def fetchone(self, name, pkey, id ):
        sql = "SELECT * FROM %s WHERE %s = '%s'" % ( name, pkey, id )
        self._execute( sql )
        return self.cursor.fetchone()

    def select(self, name, where=None):
        where = self.buildWhere( where )
        sql = "SELECT * FROM \"%s\" %s" % ( name, where )
        self._execute( sql )
        return self.cursor.fetchall()
    
    def delete(self, name, where ):
        where = self.buildWhere( where )
        sql = "DELETE FROM \"%s\" %s" % ( name, where )
        return self._execute( sql )

    def insert(self, name, key_value_pair ):
        (columns,values) = self.buildInsertList( key_value_pair )
        sql = "INSERT INTO %s (%s) VALUES (%s)" % (name, columns, values )
        self._execute( sql )
        return self.cursor.rowcount

    def update(self, name, where, updates ):
        where = self.buildWhere( where )
        sets = self.buildSets( updates )
        sql = "UPDATE \"%s\" SET %s %s" % ( name, sets, where )
        return self._execute( sql )

    def fetchColumns(self, name):
        self._execute( ( "PRAGMA table_info( '%s' )" % name ) )
        return [ column[1] for column in self.cursor.fetchall() ]

    def _execute(self, sql, *args):
        try:
            self.cursor.execute( sql, *args )
        except Error, e: 
            raise Exception( "Query Error '%s' - %s" % ( e, sql ) )

    def execute(self, sql, *args):
        self._execute( sql, *args )
        results = self.cursor.fetchall()
        return (self.cursor.description, results)

