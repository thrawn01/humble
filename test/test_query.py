import unittest, sys, os
import logging

from humble import Humble
from humble.query import *
import config

#logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

class QueryTests( unittest.TestCase ):
    def setUp(self):
        self.db = config.setUpDatabase()

    def tearDown(self):
        config.cleanUpDatabase()

    def testOperators(self):
        self.assertEquals( equal( column( 'age' ) , 28 ), ( { 'column': (None, 'age' ) }, '=', 28 ) )
        self.assertEquals( equal( column( 'last' ) , 'McBride' ), ( { 'column': (None, 'last' ) }, '=', 'McBride' ) )
        self.assertEquals( lessThan( column( 'age' ), 28 ), ( { 'column': (None, 'age' ) }, '<', 28 ) )
        self.assertEquals( greaterThan( column( 'age' ), 28 ), ( { 'column': (None, 'age' ) }, '>', 28 ) )
        
    def testWhere(self):

        self.assertEquals( where( equal( column( 'age' ), 28 ), equal( column( 'last' ), 'McBride' ) ), {
                'where': (
                    ( { 'column': (None, 'age') }, '=', 28 ), 
                    ( { 'column': (None, 'last') }, '=', 'McBride' ), 
                ) 
            })

        self.assertEquals( where( lessThan( column( 'age' ), 30 ), greaterThan( column( 'age' ), 20 )  ), { 
                'where': (
                    ( { 'column': (None, 'age') }, '<', 30 ), 
                    ( { 'column': (None, 'age') }, '>', 20 )
                )
            })

        # TODO: After delcarative layer 
        # where( Employee.age == 28 )
        #where( notEqual( 'age', 28 ) )
        #where( lessThan( 'age', 28 ) )
        #where( greaterThan( 'age', 28 )
        #where( greaterThan( 'age', 10 ), lessThan( 'age', 30 ) )
        
