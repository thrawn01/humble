import unittest, sys, os
sys.path.append( ".." )
sys.path.append( "../.." )

from humble.database.sqlite import Sqlite
import data

class TestSqlite( unittest.TestCase ):

    def setUp(self):
        self.db = Sqlite( data.db_file )

    def tearDown(self):
        os.unlink( data.db_file )

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
        self.assertEquals( self.db.fetchColumns( 'employee' ),
            [u'id', u'first', u'last', u'age', u'address'] )
   
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


