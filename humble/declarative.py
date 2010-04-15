
class Row(object): pass
class Table(Row): pass
#def __setattr__(cls, key, value):
#    print key,value
#ef __getattr__(cls, key):
#   print key

class Column(object): pass
class Int(Column): pass
class Char(Column):
    def __init__(self,size):
        try:
            self.size = int(size)
        except TypeError:
            raise TypeError( "Char( %r ) is invalid size" % type(size) )

class Text(Column): pass

