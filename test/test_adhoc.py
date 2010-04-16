import unittest, sys, os

from humble import Humble, AdhocTable 
from humble.database.sqlite import Sqlite
import data

class AdhocTests( unittest.TestCase ):

    def setUp(self):
        self.db_file = ( "/tmp/%s.db" % os.getpid() )
        self.employee_row1 = { 'first' : 'Derrick', 'last' : 'Wippler',
                          'age' : 31, 'address' : "DataPoint Drive" }
        self.employee_row2 = { 'first' : 'Brandie', 'last' : 'Marie',
                          'age' : 28, 'address' : "HelloKitty Drive" }
        self.create = """CREATE TABLE employee (
                        id      INTEGER PRIMARY KEY AUTOINCREMENT,
                        first   CHAR(30),
                        last    CHAR(30),
                        age     INTEGER,
                        address TEXT
                    ); """
        db = Sqlite( self.db_file )
        db.execute( self.create )

    def tearDown(self):
        os.unlink( self.db_file )

    def testCreate(self):
        # Tell Humble about our table without having to define it
        humble = Humble( AdhocTable( 'employee', pkey='id' ), Sqlite( self.db_file ) )

        # Create a new row object to manipulate
        employee = humble.create( 'employee' )

        # Normal Assignment
        employee.first = "Derrick"
        employee.last = "Wippler"

        employee.save()

        # Get the employee record
        #employee = humble.get( 'employee', 1 )

        #self.assertEquals( employee.first, 'Derrick' )
        #self.assertEquals( employee.last, 'Derrick' )
        #self.assertEquals( employee.age, 31 )
        #self.assertEquals( employee.address, 'DataPoint Drive' )

    def testDelete(self):
        pass
        # Tell Humble about our table without having to define it first
        #humble = Humble( AdhocTable( 'employee', pkey='id' ), Sqlite( self.db_file ) )

        # Create a new row object to manipulate
        #employee = humble.create( 'employee', fromDict=self.employee_row1 )
        #employee.save()
        #employee = humble.create( 'employee', fromDict=self.employee_row2 )
        #employee.save()

        # Get the employee record
        #employee = humble.get( 'employee', 1 )
        #employee.delete()

        #self.assertRaises( HumbleError, humble.get, 'employee', 1 )


if __name__ == "__main__":
    unittest.main()

