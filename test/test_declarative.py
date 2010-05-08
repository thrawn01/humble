import unittest, sys
sys.path.append( ".." )

from humble.declarative import Declarative, Int, Char, Text
from humble.database.sqlite import Sqlite

class Employee( Declarative ):
    __name__ = 'employee'
    id = Int()
    first = Char(30)
    last = Char(30)
    age = Int()
    address = Text()

class DelcarativeTest( unittest.TestCase ):

    def setUp(self): pass
    def tearDown(self): pass

    def testCreateTables(self):
        emp = Employee()
        #db = Sqlite( tables = [ Employee() ] )

        # Create the database
        #db.createDatabase( 'db_name' )
        # Create the tables we know about
        #db.createTable( 'db_name', 'employee' )

        #humble = Humble( db )

