""" 
    Defines the functions that create
    the query structure humble consumes
"""
__all__ = [ 'equal', 'lessThan', 'greaterThan', 'column', 'where', 'sql_and', 'sql_or' ]

def compare( left, operator, right ):
    return 

def equal( left, right ):
    return ( left, '=', right )

def lessThan( left, right ):
    return ( left, '<', right )

def greaterThan( left, right ):
    return ( left, '>', right )

def column( table, column=None ):
    if column:
        return ( 'column', table, column )
    return ( 'column', None, table )

def tuple_join( separator, args ):
    result = [ args[0] ]
    for item in args[1:]:
        result.extend( [ separator, item ] )
    return tuple( result )
    
def sql_or( *args ):
    return tuple_join( 'or', args )

def sql_and( *args ):
    return tuple_join( 'and', args )

def where( *args ):
    result = [ 'where' ]
    result.extend( [ expr for expr in args ] )
    return tuple( result )

