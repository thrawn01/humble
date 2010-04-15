import unittest, sys, os
sys.path.append( ".." )

from humble import Humble, AdhocTable 
from humble.database.sqlite import Sqlite
import data

class AdhocTests( unittest.TestCase ):

    def setUp(self):
        db = Sqlite( Data.db_file )
        db.execute( Data.table_create )

    def tearDown(self):
        os.unlink( Data.db_file )
        
    def testCreate(self):
        # Tell Humble about our table without having to define it
        humble = Humble( AdhocTable( 'employee', pkey='id' ), Sqlite( Data.db_file ) )

        # Create a new row object to manipulate
        employee = humble.create( 'employee' )

        # Normal Assignment
        employee.first = "Derrick"
        employee.last = "Wippler"

        employee.save()

        # Get the employee record
        employee = humble.get( 'employee', 1 )

        self.assertEquals( employee.first, 'Derrick' )
        self.assertEquals( employee.last, 'Derrick' )
        self.assertEquals( employee.age, 31 )
        self.assertEquals( employee.address, 'DataPoint Drive' )

    def testDelete(self):
        # Tell Humble about our table without having to define it first
        humble = Humble( AdhocTable( 'employee', pkey='id' ), Sqlite( Data.db_file ) )

        # Create a new row object to manipulate
        employee = humble.create( 'employee', fromDict=Data.employee_row1 )
        employee.save()
        employee = humble.create( 'employee', fromDict=Data.employee_row2 )
        employee.save()

        # Get the employee record
        employee = humble.get( 'employee', 1 )
        employee.delete()

        self.assertRaises( HumbleError, humble.get, 'employee', 1 )

