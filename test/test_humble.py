import unittest, sys, os
import logging

from humble import Humble
import config

#logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

class HumbleTests( unittest.TestCase ):

    def setUp(self):
        self.employee_row1 = { 'first' : 'Derrick', 'last' : 'Wippler',
                          'age' : 31, 'address' : "DataPoint Drive" }
        self.employee_row2 = { 'first' : 'Brandie', 'last' : 'Marie',
                          'age' : 28, 'address' : "HelloKitty Drive" }
        self.db = config.setUpDatabase()

    def tearDown(self):
        config.cleanUpDatabase()

    def testCreate(self):
        # Tell Humble about our table without having to define it
        humble = Humble( self.db )

        # Create a new row object to manipulate
        employee = humble.create( 'employee' )

        # Normal Assignment
        employee.first = "Derrick"
        employee.last = "Wippler"

        employee.save()

        # Get the employee record
        employee = humble.get( 'employee', 1 )

        self.assertEquals( employee.first, 'Derrick' )
        self.assertEquals( employee.last, 'Wippler' )

        # Since we didn't define these values, they are empty
        self.assertEquals( employee.age, None )
        self.assertEquals( employee.address, None )
        return humble

    def testUpdate(self):
        humble = self.testCreate()

        employee = humble.get( 'employee', 1 )

        employee.age = 31
        employee.address = "Datapoint Drive"
      
        # Since the record alread exists in the database 
        # this will preform an update
        employee.save()

        # Retrieve the employee record again
        employee = humble.get( 'employee', 1 )

        self.assertEquals( employee.first, 'Derrick' )
        self.assertEquals( employee.last, 'Wippler' )
        self.assertEquals( employee.age, 31 )
        self.assertEquals( employee.address, "Datapoint Drive" )
        return humble

    def testDelete(self):
        humble = self.testUpdate()

        employee = humble.create( 'employee', fromDict=self.employee_row2 )
        employee.save()

        # Get the employee record
        employee = humble.get( 'employee', 1 )
        employee.delete()

        self.assertRaises( Exception, humble.get, 'employee', 1 )

        employee = humble.get( 'employee', 2 )
        self.assertEquals( employee.first, 'Brandie' )
        self.assertEquals( employee.last, 'Marie' )
        self.assertEquals( employee.age, 28 )
        self.assertEquals( employee.address, "HelloKitty Drive" )

    def testInsert(self):
        humble = self.testUpdate()

        humble.insert( "employee", { 'first':'Joe', 'last':'McBride', 'age':21, 'address':"Castle Drive" } )
        humble.insert( "employee", { 'first':'Nathan', 'last':'Cassano', 'age':29, 'address':"Washington Drive" } )
        humble.insert( "employee", { 'first':'Ryan', 'last':'Springer', 'age':28, 'address':"France Drive" } )
        
        
        employee = humble.get( 'employee', 4 )
        self.assertEquals( employee.first, 'Ryan' )
        self.assertEquals( employee.last, 'Springer' )
        self.assertEquals( employee.age, 28 )
        self.assertEquals( employee.address, "France Drive" )

        self.assertRaises( Exception, humble.insert, 'employee', { 'blah':'Ryan', 'last':'Springer', 'age':28, 'address':"France Drive" } )

if __name__ == "__main__":
    unittest.main()

