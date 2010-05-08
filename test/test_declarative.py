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

    def testMetaClass(self):
        emp = Employee()
        self.assertEquals( emp.columns , ['last', 'age', 'address', 'id', 'first'] )
        self.assertEquals( emp.name , 'employee' )
        self.assertEquals( emp.__dict__ , {} )
        self.assertEquals( emp.__class__.__name__ , 'Employee' )

    def testCreateTables(self):
        pass
        #db = Sqlite( tables = [ Employee() ] )

        # Create the database
        #db.createDatabase( 'db_name' )
        # Create the tables we know about
        #db.createTable( 'db_name', 'employee' )

        #humble = Humble( db )

