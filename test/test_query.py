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
        self.assertEquals( equal( 'age', 28 ), ( ('age',), '=', 28 ) )
        self.assertEquals( lessThan( 'age', 28 ), ( ('age',), '<', 28 ) )
        self.assertEquals( greaterThan( 'age', 28 ), ( ('age',), '>', 28 ) )
        
    def testWhere(self):

        self.assertEquals( where( equal( 'age', 28 ) ), {
                'where': (
                    (('age',), '=', 28 ),
                ) 
            })

        self.assertEquals( where( lessThan( 'age', 30 ), greaterThan( 'age', 20 )  ), { 
                'where': (
                    (('age',), '<', 30), 
                    (('age',), '>', 20)
                )
            })

        # TODO: After delcarative layer 
        # where( Employee.age == 28 )
        #where( notEqual( 'age', 28 ) )
        #where( lessThan( 'age', 28 ) )
        #where( greaterThan( 'age', 28 )
        #where( greaterThan( 'age', 10 ), lessThan( 'age', 30 ) )
        
