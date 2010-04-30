import sqlite3
from sqlite3 import Error
import logging

from humble import Table, Struct
from humble.database import DatabaseInterface, Int, Text, Column

log = logging.getLogger("humble_sql")

def dictFactory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

class SqlGenerator( object ):    

    @classmethod
    def where( self, struct ):
        return " WHERE %s " % self.conditionals( struct['where'] )

    @classmethod
    def conditionals( self, struct ):
        result = []
        for left, operator, right in struct:
            result.append( "%s %s %s" % ( self.toString( left ), operator, self.toString( right ) ) )
        return " AND ".join( result )

    @classmethod
    def toString( self, struct ):
        try:
            try:
                (table,name) = struct
                return "%s.%s" % ( table, name )
            except ValueError:
                return str(struct[0])
        except IndexError:
            raise Exception( "Column Identifer must be a tuple ( table, name ) or ( name, )" )
        except TypeError:
            # Must be a literal ( string, int, etc.. )
            return str(struct)
            

class Sqlite( DatabaseInterface ):

    def __init__(self, tables, file ):
        log.debug( "Connect( %s )" % file )
        # Open up the sqlite file
        self.connection = sqlite3.connect( file )
        # Sqlite DBI 2.0 extension - use dictFactory to create result rows
        self.connection.row_factory = dictFactory
        # Grab our cursor
        self.cursor = self.connection.cursor()

        # TODO: Add the rest of the types
        self.type_mapping = { 'INTEGER' : Int() }
        self.tables = {}

        # Maybe we just passed in 1 table, instead of a list of tables
        if isinstance( tables, Table ):
            tables = [tables]

        # Create a place for storing data about the table
        for table in tables:
            self.tables[table.__name__] = Struct( name=table.__name__, pkey=table.__pkey__, columns=[], cached=False )

    def getTable(self, name):
        """ Return the table object called 'name' """
        try:
            table = self.tables[name]
            # Column names cached already?
            if not table.cached:
                # fetch the column names from the DB
                table.columns = self.fetchColumns( name )
                table.cached = True
            return table

        except (ValueError,KeyError):
            raise Exception( "Sqlite() unknown table '%s'; forgot to add Sqlite( tables=[ Table() ] )?" % name )

    def fetchone(self, name, pkey, id ):
        sql = "SELECT * FROM %s WHERE %s = '%s'" % ( name, pkey, id )
        log.debug( sql )
        self._execute( sql )
        return self.cursor.fetchone()

    def select(self, name, where=None):
        where = SqlGenerator.where( where )
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
        result = [ Column( name=row['name'], type=self.toType( row['type'], row['dflt_value'] ) )
                   for row in self.cursor.fetchall() ]
        if not result:
            raise Exception( "fetchColumns(%s) returned nothing; Non-existant table?" % name )
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

    def toType(self, field, default):
        # If we were asked for a type we don't know about
        if not field in self.type_mapping.keys():
            # Just return Text()
            return Text(default)
        return self.type_mapping[field].__class__(default)

