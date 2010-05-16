import unittest, sys
sys.path.append( ".." )

from humble.declarative import Declarative, Int, Char, Text
from humble.database.sqlite import Sqlite
import config

class Employees( Declarative ):
    __name__ = 'employees'
    id = Int()
    first = Char(30)
    last = Char(30)
    age = Int()
    address = Text()

class Contacts( Declarative ):
    id = Int()
    type = Char(6)
    number = Char(10)

class DelcarativeTest( unittest.TestCase ):

    def setUp(self): pass
    def tearDown(self): pass

    def testMetaClass(self):

        emp = Employees()

        # Ensure the columns all exist, ( regardless of order )
        for column in ['last', 'age', 'address', 'id', 'first']:
            self.assertTrue( column in emp.__columns__ )
        self.assertEquals( emp.__name__ , 'employees' )
        self.assertEquals( emp.__dict__ , {} )
        self.assertEquals( emp.__class__.__name__ , 'Employees' )

        contact = Contacts()

        # Ensure the columns all exist, ( regardless of order )
        for column in ['id', 'type', 'number']:
            self.assertTrue( column in contact.__columns__ )
        self.assertEquals( contact.__name__ , 'Contacts' )
        self.assertEquals( contact.__dict__ , {} )
        self.assertEquals( contact.__class__.__name__ , 'Contacts' )

    def testCreateTables(self):
        db = Sqlite( tables = [ Employees() ], file=config.db_name )

        # Create the database
        #db.createDatabase( 'db_name' )
        # Create the tables we know about
        #db.createTable( 'db_name', 'contactloyee' )

        #humble = Humble( db )

