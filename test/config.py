from humble.database.sqlite import Sqlite
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
    database = Sqlite( db_name )
    database.execute( sql )
    return database

def cleanUpDatabase():
    os.unlink( db_name )

