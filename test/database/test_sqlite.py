import unittest, sys, os
sys.path.append( ".." )
sys.path.append( "../.." )

from humble.database import DatabaseInterface, Int, Text, Column
from humble.database.sqlite import Sqlite
import data

class TestSqlite( unittest.TestCase ):

    def setUp(self):
        self.db_name = "/tmp/%s.db" % os.getpid()
        self.db = Sqlite( self.db_name )

    def tearDown(self):
        os.unlink( self.db_name )

    def createTable(self):
        create = """CREATE TABLE employee (
                        id      INTEGER PRIMARY KEY AUTOINCREMENT,
                        first   CHAR(30),
                        last    CHAR(30),
                        age     INTEGER,
                        address TEXT
                    ); """
        self.db.execute( create )

    def testFetchColumns(self):
        self.createTable()
        result = self.db.fetchColumns( 'employee' )
        self.assertEquals( result[0].name, 'id' )
        self.assertEquals( result[4].name, 'address' )

        #    [ Column( type=Int( default=0 ), name=u'id' ), 
        #      Column( type=Text( default='' ), name=u'first' ), 
        #      Column( type=Text( default='' ), name=u'last' ), 
        #      Column( type=Int( default=0 ), name=u'age' ), 
        #      Column( type=Text( default='' ), name=u'address' )] )
        #[u'id', u'first', u'last', u'age', u'address'] )
   
    def testInsertAndFetch(self):
        self.createTable()

        self.db.insert( "employee", { 'first' : 'Derrick', 
                                      'last' : 'Wippler',
                                      'age' : 31, 
                                      'address' : "DataPoint Drive" } )
        self.assertEquals( self.db.fetchone( name="employee", pkey='id', id=1 ),
                (1, u'Derrick', u'Wippler', 31, u'DataPoint Drive') )

    def testUpdate(self):
        self.testInsertAndFetch()

        self.db.update( name='employee', where={ 'id': 1 }, updates={ 'first' : 'Thrawn' } )

        self.assertEquals( self.db.fetchone( name="employee", pkey='id', id=1 ),
                (1, u'Thrawn', u'Wippler', 31, u'DataPoint Drive') )

    def testSelect(self):
        self.createTable()
        self.db.insert( "employee", { 'first' : 'Derrick', 
                                      'last' : 'Wippler',
                                      'age' : 31, 
                                      'address' : "DataPoint Drive" } )
        self.db.insert( "employee", { 'first' : 'Brandie', 
                                      'last' : 'Wippler',
                                      'age' : 29, 
                                      'address' : "HelloKitty Drive" } )

        results = self.db.select( "employee", where={ 'last' : 'Wippler' } )
        self.assertEquals( results, 
                [(1, u'Derrick', u'Wippler', 31, u'DataPoint Drive'), 
                (2, u'Brandie', u'Wippler', 29, u'HelloKitty Drive')] )

    def testdelete(self):
        self.testInsertAndFetch()
        
        self.db.delete( name='employee', where={ 'id': 1 } )

        self.assertEquals( self.db.fetchone( name="employee", pkey='id', id=1 ), None )


