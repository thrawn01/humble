import sqlite3
from sqlite3 import Error
import logging

from humble import Table, Struct
from humble.database import DatabaseInterface, Int, Text, Column
from humble.util import Util

log = logging.getLogger("humble_sql")

def SafeNone(object):
    def __init__(self, exception ):
        self.exception = exception

    def __getattr__(self, attr):
        raise self.exception
        
def dictFactory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

class SqlGenerator( object ):    

    def __init__( self, parent ):
        self.parent = parent

    def exprToString( self, expr ):
        try:
            # A string literal
            if type( expr ) == str:
                return expr 

            # Column expressions
            if expr[0] == 'column':
                return self.columnToString( expr[1:] )
            
            # Everything else, is evaluated and joined
            return " ".join( [ "%s" % self.exprToString( e ) for e in expr ] )

        except TypeError:
            return str( expr )
            
    def columnToString( self, expr ):
        try:
            (table,name) = expr
            if table:
                return "%s.%s" % (table, name)
            return "%s.%s" % ( self.findColumn( name ), name )
        except IndexError:
            raise Exception( "Column Identifer must be a tuple { column: ( table, name ) } ; "
                             "Got '%s' instead" %  expr.__class__.__name__ )

    def findColumn( self, name ):
        result = []

        # Search thru the available tables for a matching column name
        for key,table in self.parent.tables.iteritems():
            # If the column exists in this table, record it
            if name in table.__columns__:
                result.append( table.__name__ )

        if len( result ) > 1:
            raise Exception( "Column '%s' is ambigous; you must specify a table name" % name )
        if len( result ) == 0:
            raise Exception( "Unknown column '%s'" % name )
        return result[0]


class Sqlite( DatabaseInterface ):

    def __init__(self, tables, database ):
        log.debug( "Connect( %s )" % database )
        self.cursor = SafeNone( Exception( "Sqlite() - Connect to a database before running a query" ) )
        self.database = database
        self.connection = None
        self.tables = {}

        # Maybe we just passed in 1 table, instead of a list of tables
        if not Util.isList( tables ):
            tables = [ tables ]

        for table in tables:
            self.tables[table.__name__] = table

    def connect(self):
        # Open up the sqlite file
        self.connection = sqlite3.connect( self.database )
        # Sqlite DBI 2.0 extension - use dictFactory to create result rows
        self.connection.row_factory = dictFactory
        # Grab our cursor
        self.cursor = self.connection.cursor()

        # Ensure our table objects are complete
        for name,table in self.tables.iteritems():
            # If the columns are not specified
            if not table.__columns__:
                # Ask the database about the columns
                # TODO: Get more detail about the table
                #       Fill out the entire Table() object
                table.__columns__ = self.fetchColumns( name )
                
            self.tables[name] = table
        
        self.generator = SqlGenerator( parent=self )

    def getTableInfo(self, name):
        """ Return some select information about a table """
        table = self.getTable( name )
        return Struct( name=table.__name__, pkey=table.__pkey__, columns=table.__columns__ )

    def getTable(self, name):
        """ Return the table object for requested table """
        try:
            return self.tables[name]
        except (ValueError,KeyError):
            raise Exception( "Sqlite() - Unknown table '%s'; forgot to add Sqlite( tables=[ Table() ] )?" % name )

    def fetchone(self, name, pkey, id ):
        sql = "SELECT * FROM %s WHERE %s = '%s'" % ( name, pkey, id )
        log.debug( sql )
        self._execute( sql )
        return self.cursor.fetchone()

    def select(self, name, where=None):
        where = self.generator.exprToString( where )
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
        sql = "UPDATE \"%s\" SET %s %s" % ( name, sets, where )
        log.debug( sql )
        return self._execute( sql )

    def fetchColumns(self, name):
        sql = ( "PRAGMA table_info( '%s' )" % name )
        log.debug( sql )
        self._execute( sql )
        result = [ row['name'] for row in self.cursor.fetchall() ]
        if not result:
            raise Exception( "'%s' - returned nothing; Non-existant table?" % sql )
        return result

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

    def createDatabase(self, name ):
        pass

    def createTableStmt(self, table ):
        columns = []
        for key in table.__columns__:
            column = table.__getattr__(key)
            columns.append( "%s     %s" % ( key, column ) )
        
        sql = "CREATE TABLE %s ( %s )" % ( table.__name__, ",".join( columns ) )
        return sql

    def toType(self, field, default):
        # If we were asked for a type we don't know about
        if not field in self.type_mapping.keys():
            # Just return Text()
            return Text(default)
        return self.type_mapping[field].__class__(default)

