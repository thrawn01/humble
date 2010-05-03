
import unittest, sys, os
import logging

from humble import Humble
from humble.query import *
import config

#logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

class SelectTests( unittest.TestCase ):

    def setUp(self):
        self.db = config.setUpDatabase()

    def tearDown(self):
        config.cleanUpDatabase()

    def createDataSet(self):
        humble = Humble( self.db )
        humble.insert( "employee", { 'first':'Joe', 'last':'McBride', 'age':21, 'address':"Castle Drive" } )
        humble.insert( "employee", { 'first':'Nathan', 'last':'Cassano', 'age':29, 'address':"Washington Drive" } )
        humble.insert( "employee", { 'first':'Ryan', 'last':'Springer', 'age':28, 'address':"France Drive" } )
        return humble

    def testSimpleWhere(self):
        humble = self.createDataSet()
        
        result = humble.select( 'employee', where( equal( column( 'age' ), 28 ) ) )
        self.assertEqual( result[0].first, 'Ryan' )
        self.assertEqual( result[0].last, 'Springer' )
        self.assertEqual( result[0].age, 28 )

        result = humble.select( 'employee', where( equal( column( 'age' ), 28 ), equal( column( 'last' ), 'McBride' ) ) )
        self.assertEqual( result[0].first, 'Ryan' )
        #self.assertEqual( result[0].last, 'Springer' )
        #self.assertEqual( result[0].age, 28 )

        #self.assertEqual( result[1].first, 'Joe' )
        #self.assertEqual( result[1].last, 'McBride' )
        #self.assertEqual( result[1].age, 21 )
