
class Util(object):

    @classmethod
    def replace( self, haystack, needles, button ):
        """ Replace all occurances of needles in haystack with button """
        for sub in needles:
            haystack = haystack.replace( sub, button )
        return haystack

    @classmethod
    def isList( self, kind ):
        try:
            kind[0]
            return True
        except TypeError:
            return False

