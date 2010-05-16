
class Column(object):
    def __repr__(self):
        return "%s" % self.type
        
class Int(Column):
    type = "INTEGER"

class Char(Column):
    type = "TEXT"
    def __init__(self,size):
        try:
            self.size = int(size)
            Column.__init__(self)
        except TypeError:
            raise TypeError( "Char( %r ) is invalid size" % type(size) )
    def __repr__(self):
        return "%s( %s )" % ( self.type, self.size )

class Text(Column):
    type = "TEXT"

class DeclarativeType(type):
    def __new__(cls, name, bases, attrs):
        new_attrs = {}
        
        # Don't transform if this is called on the BaseClass
        if name.startswith('Declarative'):
            return super(DeclarativeType, cls).__new__(cls, name, bases, attrs)

        # If user didn't supply name
        if not attrs.get( '__name__', None ):
            # Use the name of the class
            new_attrs['__name__'] = name

        # Transform into an object that looks like a Table() object
        columns = []
        dict = {}
        for key, value in attrs.iteritems():
            if not key in [ '__module__', '__name__' ]:
                columns.append( key )
                dict[key] = value
                continue
            new_attrs[key] = value

        # TODO: Figure out the primary key

        new_attrs['__columns__'] = columns
        # TODO: Must be a better way to do this
        new_attrs['__classdict__'] = dict

        return super(DeclarativeType, cls).__new__(cls, name, bases, new_attrs )

    #def __init__(self, name, bases, attrs):
        #super(DeclarativeType, self).__init__(name, bases, attrs)
        #print "attrs ", attrs

class Declarative:
    __metaclass__ = DeclarativeType

    def __getattr__( self, attr ):
        return self.__classdict__[attr]

