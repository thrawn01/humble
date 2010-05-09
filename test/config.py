from humble.database.sqlite import Sqlite
from humble import Table
import sqlite3
import os

db_name = "/tmp/%s.db" % os.getpid()

# ---------------------------------
# For SQL-lite testing
# ---------------------------------
def setUpDatabase():
    sql = """CREATE TABLE employee (
                id      INTEGER PRIMARY KEY AUTOINCREMENT,
                first   CHAR(30),
                last    CHAR(30),
                age     INTEGER,
                address TEXT
                ); """

    # Create the table first, Sqlite() will ask the db about the columns
    connection = sqlite3.connect( db_name )
    cursor = connection.cursor()
    cursor.execute( sql )
    
    database = Sqlite( tables = [ Table( 'employee', pkey='id' ) ], file=db_name )
    return database

def cleanUpDatabase():
    os.unlink( db_name )

