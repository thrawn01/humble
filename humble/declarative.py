
class Row(object): pass
#class Table(Row): pass
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


def make_hook(f):
    """Decorator to turn 'foo' method into '__foo__'"""
    f.is_hook = 1
    return f

class DeclarativeType(type):
    def __new__(cls, name, bases, attrs):
        new_attrs = {}
        
        # Don't transform if this is called on the BaseClass
        if name.startswith('Declarative'):
            return super(DeclarativeType, cls).__new__(cls, name, bases, attrs)

        # If user didn't supply name
        if not attrs.get( '__name__', None ):
            # Use the name of the class
            new_attrs['name'] = name
        else:
            new_attrs['name'] = attrs['__name__']
            del attrs['__name__']

        # Transform into an object that looks like a Table() object
        columns = []
        for key, value in attrs.iteritems():
            if not key in [ '__module__' ]:
                columns.append( key )
                continue
            new_attrs[key] = value


        # TODO: Figure out the primary key

        new_attrs['columns'] = columns

        return super(DeclarativeType, cls).__new__(cls, name, bases, new_attrs )

    #def __init__(self, name, bases, attrs):
        #super(DeclarativeType, self).__init__(name, bases, attrs)

        # classregistry.register(self, self.interfaces)
        #print "Would register class %s now." % self

    def __add__(self, other):
        class AutoClass(self, other):
            pass
        return AutoClass
        # Alternatively, to autogenerate the classname as well as the class:
        # return type(self.__name__ + other.__name__, (self, other), {})

    def unregister(self):
        # classregistry.unregister(self)
        print "Would unregister class %s now." % self

class Declarative:
    __metaclass__ = DeclarativeType

#class NoneSample(MyObject):
    #pass

# Will print "NoneType None"
#print type(NoneSample), repr(NoneSample)

#class Example(MyObject):
#    def __init__(self, value):
#        self.value = value
#    @make_hook
#    def add(self, other):
#        return self.__class__(self.value + other.value)
#
# Will unregister the class
#Example.unregister()

#inst = Example(10)
# Will fail with an AttributeError
#inst.unregister()

#print inst + inst
#class Sibling(MyObject):
#    pass

#ExampleSibling = Example + Sibling
# ExampleSibling is now a subclass of both Example and Sibling (with no
# content of its own) although it will believe it's called 'AutoClass'
#print ExampleSibling
#print ExampleSibling.__mro__

