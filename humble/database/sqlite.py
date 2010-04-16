import sqlite3
from sqlite3 import Error
import logging

from humble.database import DatabaseInterface

log = logging.getLogger("humble_sql")

class Sqlite( DatabaseInterface ):

    def __init__(self, file ):
        log.debug( "Connect( %s )" % file )
        # Open up the sqlite file
        self.connection = sqlite3.connect( file )
        # Grab our cursor
        self.cursor = self.connection.cursor()

    def fetchone(self, name, pkey, id ):
        sql = "SELECT * FROM %s WHERE %s = '%s'" % ( name, pkey, id )
        log.debug( sql )
        self._execute( sql )
        return self.cursor.fetchone()

    def select(self, name, where=None):
        where = self.buildWhere( where )
        sql = "SELECT * FROM \"%s\" %s" % ( name, where )
        log.debug( sql )
        self._execute( sql )
        return self.cursor.fetchall()
    
    def delete(self, name, where ):
        where = self.buildWhere( where )
        sql = "DELETE FROM \"%s\" %s" % ( name, where )
        log.debug( sql )
        return self._execute( sql )

    def insert(self, name, key_value_pair ):
        (columns,values) = self.buildInsertList( key_value_pair )
        sql = "INSERT INTO %s (%s) VALUES (%s)" % (name, columns, values )
        log.debug( sql )
        self._execute( sql )
        return self.cursor.rowcount

    def update(self, name, where, updates ):
        where = self.buildWhere( where )
        sets = self.buildSets( updates )
        log.debug( sql )
        sql = "UPDATE \"%s\" SET %s %s" % ( name, sets, where )
        return self._execute( sql )

    def fetchColumns(self, name):
        sql = ( "PRAGMA table_info( '%s' )" % name )
        log.debug( sql )
        self._execute( sql )
        return [ column[1] for column in self.cursor.fetchall() ]

    def _execute(self, sql, *args):
        try:
            self.cursor.execute( sql, *args )
        except Error, e: 
            raise Exception( "Query Error '%s' - %s" % ( e, sql ) )

    def execute(self, sql, *args):
        log.debug( sql )
        self._execute( sql, *args )
        results = self.cursor.fetchall()
        return (self.cursor.description, results)

