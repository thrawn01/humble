from DB.Connection import db
from humble.database import DatabaseInterface

class Rackspace(DatabaseInterface):
    
    def __init__(self):
        self.cursor = db.Cursor
        Database.__init__(self)

    def fetchone(self, table, id ):
        sql = "SELECT * FROM %s WHERE %s = '%s'" % ( table.name, table.pkey, id )
        self.cursor.execute( sql )
        result = self.cursor.fetchone()
        if not result:
            raise Exception( "SQL Returned no results - %s" % sql )
        return result

    def select(self, table, where=None):
        where = self.buildWhere( where )
        sql = "SELECT * FROM \"%s\" %s" % ( table.name, where )
        self.cursor.execute( sql )
        results = self.cursor.fetchall()
        if not results:
            raise Exception( "SQL Returned no results - %s" % sql )
        return results
    
    def delete(self, table_name, where ):
        where = self.buildWhere( where )

        sql = "DELETE FROM \"%s\" %s" % ( table_name, where )
        return self.cursor.execute( sql )

    def insert(self, table_name, key_value_pair ):
        (columns,values) = CoreDb.buildInsertList( key_value_pair )
       
        sql = "INSERT INTO %s (%s) VALUES (%s)" % (table_name, columns, values )
        return self.cursor.execute( sql )

    def update(self, table_name, where, updates ):
        where = self.buildWhere( where )
        sets = self.buildSets( updates )
        sql = "UPDATE \"%s\" SET %s %s" % ( table_name, sets, where )
        return self.cursor.execute( sql )
        
    def fetchColumns(self, table):
        sql = "SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = %s"
        self.cursor.execute( sql, (table.name,) )
        results = self.cursor.fetchall()
        if not results:
            raise Exception( "Unable to get column names for '%s' - %s" % ( table.name, sql ) )
       
        return [ column[0] for column in results ]

    def commit(self):
        db.commit()
        
