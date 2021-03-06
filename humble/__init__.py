""" 
    Humble Implements a Simple Active Record Pattern
    for a very light layer over database rows 
"""
from humble.util import Util

class Struct(object):
    def __init__(self, **attrs):
        for name,value in attrs.items():
            setattr( self, name, value)

    def __repr__(self):
        members = [ "%s=%r" % (key,value) for key,value in self.__dict__.items() ]
        return "%s( %s )" % (self.__class__.__name__, ",".join( members ) )

class Row(object):

    def __init__(self, database, name, pkey, fromDict=None, new=False, withValues=False):
        self.__dict__['__name__'] = name
        self.__dict__['__pkey__'] = pkey
        self.__dict__['__database__'] = database
        self.__dict__['__updates__'] = { }
        self.__dict__['__isNew__'] = new 

        self.__dict__.update( fromDict )
        if withValues:
            self.__updates__.update( fromDict )
                
    def __setattr__(self,attr,value):
        "Saving new values to the object"
        if not attr in self.__dict__:
            raise Exception( "Table '%s' has no row named '%s'" % 
                    ( self.__name__, attr ) )

        # Save to the attribute
        self.__dict__[attr] = value
        self.__updates__[attr] = value

    def __str__(self):
        result = []
        for key,value in self.__dict__.items():
            # Skip our private variables
            if key in ['__database__', '__name__', '__pkey__', '__updates__']: continue
            result.append( "  %s : %s" % (key,value) )
        return "%s ( %s )" % (self.__name__, "\n".join(result) )

    def delete(self):
        "Ask our parent to delete us, ( this doesn't invalidate us ) "
        where = { self.__pkey__ : self.__dict__[self.__pkey__] }
        return self.__database__.delete( self.__name__, where )

    def save(self):
        if self.__isNew__:
            # Insert the fields set on this object
            return self.__database__.insert( self.__name__, self.__updates__ )

        # Ask our parent to save the fields we changed
        where = { self.__pkey__ : self.__dict__[self.__pkey__] }
        result = self.__database__.update( self.__name__, where, self.__updates__ )
        self.__dict__['__updates__'] = []
        return result

    def toDict(self):
        temp = self.__dict__
        temp.update( self.__updates__ )
        return temp


class Table(object):

    def __init__(self, name, pkey, columns=[]):
        self.__name__ = name
        self.__pkey__ = pkey
        self.__columns__ = columns


class Humble(object):
    
    def __init__(self, databases):
        self.databases = databases

        # Maybe we just passed a database, instead of a list of databases
        if not Util.isList( databases ):
            self.databases = [ databases ]

        # TODO: Postpone this until we actually access the database
        for database in self.databases:
            database.connect()

    def get(self, name, id):
        return self.fetchone(name, id)

    def getDatabase(self, name ):
        # TODO: Make this faster, by using a hash
        for database in self.databases:
            result = database.getTable( name )
            if result:
                return database
        raise Exception( "Humble() - Unknown table '%s'; forgot to add table to database object?" % name )

    def fetchone(self, name, id):
        database = self.getDatabase( name )
        table = database.getTableInfo( name )

        # Ask the database layer to fetch 1 row
        result = database.fetchone( table.name, table.pkey, id )
        if not result:
            raise Exception( "Humble() - fetchone( table=%s, pkey=%s ) returned None; non-existant row?" % \
                    (table.name, table.pkey ) )
        # Return the row
        return Row( database, table.name, table.pkey, fromDict=result )
    
    def select(self, name, where=None):
        database = self.getDatabase( name )
        table = database.getTableInfo( name )
   
        # Ask the database layer to build and execute the query
        results = database.select( table.name, where )
        #TODO: if result = None

        # Return the rows
        return [ Row( database, table.name, table.pkey, fromDict=result ) for result in results ]

    def delete(self, name, id ):
        database = self.getDatabase( name )
        table = database.getTableInfo( name )

        where = { table.pkey : id }
        return database.delete( table.name, where )

    def insert(self, name, fromDict={} ):
        database = self.getDatabase( name )
        table = database.getTableInfo( name )

        # Validate the fields first
        for key,value in fromDict.iteritems():
            if not key in table.columns:
                raise Exception( "Table '%s' has no such column '%s'" % ( name, key ) )

        # Insert the fields set on this object
        return database.insert( name, fromDict )
  
    def create(self, name, fromDict={}):
        rowDict = {}

        database = self.getDatabase( name )
        table = database.getTableInfo( name )
        for name in table.columns:
            rowDict[name] = fromDict.get( name, None )

        # If fromDict did NOT include the primary key value
        if not table.pkey in fromDict:
            # Don't give it a default
            rowDict[table.pkey] = None

        # Tel the row object this is a 'new' row
        return Row( database, table.name, table.pkey, fromDict=rowDict, new=True, withValues=True )

    # TODO: Figure out a better way to do this, 
    # ( Maybe pass in the name of the database ? )
    def commit(self, name):
        database = self.getDatabase( name )
        database.commit()

