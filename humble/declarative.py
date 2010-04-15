
class Table(object): pass

class Int(object): pass
class Char(object):
    def __init__(self,size):
        try:
            self.size = int(size)
        except TypeError:
            raise TypeError( "Char( %r ) is invalid size" % type(size) )

class Text(object): pass

