
class DatabaseInterface(object):

    def __init__( self ):
        self.cursor = None
        self.connection = None
    
    def getName( self, table ):
        return table.__name

    def getPkey( self, table ):
        return table.__pkey

    def mogrify(self, sql, *args):
        """ Return a query string after arguments binding. 
        The string returned is exactly the one that would be 
        sent to the database running the execute() method or similar."""
        try:
            return self.cursor.mogrify( sql, *args)
        except AttributeError:
            return sql

    def buildWhere( self, where ):
        if not where:
            return ""

        try:
            result = [ 'WHERE' ]
            for key,value in where.items():
                conditional = '"%s" = %s' % (key, self.escape(value))
                result.append( conditional )
            return ' '.join( result ) 
        except TypeError:
            raise
            raise Exception( "Where must be a dict of column and values" )

    def buildSets( self, key_value ):
        if not key_value:
            return ""

        try:
            result = [ ]
            for key,value in key_value.items():
                set = '"%s" = %s' % (key, self.escape(value))
                result.append( set )
            return ','.join( result ) 
        except TypeError:
            raise
            raise Exception( "Set must be a dict of column and values" )
    
    def buildInsertList( self, key_values ):
        if not key_values:
            return ( "", "" )

        try:
            columns = [ ]
            values = [ ]
            for key,value in key_values.items():
                columns.append( key )
                values.append( str(self.escape(value)) )

            return ( ','.join( columns ), ','.join( values ) )

        except TypeError:
            raise
            raise Exception( "key_values must be a dict of column and values" )

    def tableName( self, query ):
        """ Attempt to figure out what table a query is using """
        query = self.replace( query, [ "\n", "\\\n", "\\n", "\\\n", ], " " )
        match = re.search( "(FROM|from)\s+(\S*)", query )
        if match == None:
            return ""
        result = match.groups()[1]
        return result.replace( '"', '' )
    
    def escape( self, value ):
        try:
            chars = list(value)
            types = {'"':'\\"', "'":"\\'", "\0":"\\\0", "\\":"\\\\"}
            for i in xrange(len(chars)):
                chars[i] = types.get(chars[i], chars[i])
            return ( "'%s'" % ''.join(chars) )
        except TypeError:
            # If we get an error, might indicate 'value' is an int or bool
            if isinstance( value, bool ):
                if value: 
                    return "TRUE"
                return "FALSE"
            if isinstance( value, int ):
                return int(value)
            return value

