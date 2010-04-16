""" 
    Implements a Simple Active Record Pattern
    for a very light layer over database rows 

    Current Usage:

        # Create the active record singleton
        humble = Humble( Table( 'notification_task', pkey='id' ) )

        # Get a row
        row = humble.fetchone( 'notification_task', '22' )

        # Use the row
        print row.id

        # Delete the row
        row.delete()

        # Commit the transation
        humble.commit()

        # Select with where
        rows = humble.select( 'notification_task', where = { 'notification_id' : '23' } )

        for row in rows:
            print row.id, row.account

        # Get a row
        row = humble.fetchone( 'notification_task', '22' )

        row.account = 12345
        row.save()

        # Commit the transation
        humble.commit()

"""

class Row(object):

    def __init__(self, parent, table, tuple=None, new=False):
        self.__dict__['__table__'] = table
        self.__dict__['__parent__'] = parent
        self.__dict__['__updates__'] = { }
        self.__dict__['__isNew__'] = new 

        # Merge the table names and tuples into the object dictionary
        for i in range(0, (len(tuple))):
            self.__dict__[table.__columns__[i]] = tuple[i]
            
    def __setattr__(self,attr,value):
        "Saving new values to the object"
        if not attr in self.__dict__:
            raise Exception( "Table '%s' has no row named '%s'" % 
                    ( self.__table__.__dict__['__name__'], attr ) )

        # Save to the attribute
        self.__dict__[attr] = value
        self.__updates__[attr] = value

    def __str__(self):
        result = []
        for key,value in self.__dict__.items():
            # Skip our private variables
            if key in ['__parent__', '__table__', '__updates__']: continue
            result.append( "  %s : %s" % (key,value) )
        return "%s ( %s )" % (self.__table__.__name__, "\n".join(result) )

    def delete(self):
        "Ask our parent to delete us, ( this doesn't invalidate us ) "
        where = { self.__table__.pkey : self.__dict__[self.__table__.pkey] }
        return self.__parent__.database.delete( self.__table__.name, where )

    def save(self):
        if self.__isNew__:
            # Insert the fields set on this object
            return self.__parent__.database.insert( self.__table__.__name__, self.__updates__ )

        # Ask our parent to save the fields we changed
        where = { self.__table__.__pkey__ : self.__dict__[self.__table__.__pkey__] }
        return self.__parent__.database.update( self.__table__.__name__, where, self.__updates__ )

    def toDict(self):
        return self.__dict__


class Table(object):

    def __init__(self, **kwargs):
        self.__dict__['__columns__'] = []

        # TODO: Figure this out from declarative
        #self.__dict__['__name__'] = name
        #self.__dict__['__pkey__'] = pkey

    def __setColumns__( self, names ):
        self.__dict__['__columns__'].extend( names )

    def __getColumns__(self):
        return self.__dict__['__columns__']


class AdhocTable(Table):

    def __init__(self, name, pkey, columns=[]):
        self.__dict__['__name__'] = name
        self.__dict__['__pkey__'] = pkey
        Table.__init__(self)


class Humble(object):
    
    def __init__(self, tables, database):
        self.tables = {}
        self.database = database

        # Maybe we just passed in 1 table, instead of a list of tables
        if isinstance( tables, Table ):
            tables = [tables]
        
        self.addTables( tables )

    def addTables(self, tables):
        " Figure out the names of the columns for each table we add "
        for table in tables:
            table.__setColumns__( self.database.fetchColumns( table.__name__ ) )
            self.tables[table.__name__] = table

    def getTable(self, name):
        """ Return the table object called 'name' """
        try:
            return self.tables[name]
        except (ValueError,KeyError):
            raise Exception( "Humble doesn't know about table '%s'" % name )

    def get(self, table_name, id):
        return self.fetchone(table_name, id)

    def fetchone(self, table_name, id):
        # get the information on this table
        table = self.getTable( table_name )

        # Ask the database layer to fetch 1 row
        result = self.database.fetchone( table.__name__, table.__pkey__, id )
        # Return the row
        return Row( self, table, result )
    
    def select(self, table_name, where=None):
        # get the information on this table
        table = self.getTable( table_name )
   
        # Ask the database layer to build and execute the query
        results = self.database.select( table, where )

        # Return the rows
        return [ Row( self, table, result ) for result in results ]

    def delete(self, table_name, id ):
        # Get the information on this table
        table = self.getTable( table_name )

        where = { table.pkey : id }
        return self.database.delete( table.name, where )

    def insert(self, obj ):
        where = { obj.__table__.__pkey__ : obj.__dict__['__pkey__'] }
        return self.database.insert( obj.__table__.__name__, where, obj.__updates__ )
  
    def create(self, name):
        table = self.getTable( name )
        # Generate an empty dataset for our columns
        data_set = [ '' for column in table.__getColumns__() ]
        # Mark the row as "new"
        return Row( self, table, data_set, new=True )

    def commit(self):
        self.database.commit()

