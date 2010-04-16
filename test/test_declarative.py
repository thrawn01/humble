import unittest, sys
sys.path.append( ".." )

from humble.declarative import Table, Int, Char, Text
from humble.database.sqlite import Sqlite

class Employee( Table ):
    id = Int()
    first = Char(30)
    last = Char(30)
    age = Int()
    address = Text()

class DelcarativeTest( unittest.TestCase ):

    def setUp(self): pass
    def tearDown(self): pass

    def testInit(self):
        employee = Employee()
        #print dir(employee)

