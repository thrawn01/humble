
import unittest, sys, os
sys.path.append( ".." )
sys.path.append( "../.." )

from humble.database.sqlite import SqlGenerator
from humble import Table, Struct

class TestSqliteSqlGenerator( unittest.TestCase ):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testExprToString(self):
        sql = SqlGenerator( parent = Struct( tables= { 'employee' : Table( name='employee', pkey='id', columns=[ 'id', 'first', 'last', 'age' ] ) } ) )

        self.assertEquals( sql.exprToString( 
            ( 'WHERE', 
                ( 'column', None, 'last' ), "=", "'McBride'" ) ),

                "WHERE employee.last = 'McBride'" )

        self.assertEquals( sql.exprToString( 
            ('WHERE',
                 (('column', None, 'age'), '=', 28),
                 'or',
                 (('column', None, 'age'), '=', 29)) ),

            "WHERE employee.age = 28 or employee.age = 29" 
        )

