import unittest, sys
sys.path.append( ".." )

from humble.util import Util

class UtilTest( unittest.TestCase ):

    def setUp(self): pass
    def tearDown(self): pass

    def testIsList(self):
        self.assertTrue( Util.isList( [ 1 ] ) )
        self.assertTrue( Util.isList( ( 1, ) ) )
        self.assertEqual( Util.isList( 1 ), False )

