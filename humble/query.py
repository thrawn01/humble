""" 
    Defines the functions that create
    the query structure humble consumes
"""
__all__ = [ 'equal', 'lessThan', 'greaterThan', 'where' ]

def toTuple( string ):
    try:
        return tuple( string.split(".") )
    except AttributeError:
        # Might be an integer
        return string

def compare( left, operator, right ):
    return ( toTuple( left ), operator, toTuple( right ) )

def equal( left, right ):
    return compare( left, '=', right )

def lessThan( left, right ):
    return compare( left, '<', right )

def greaterThan( left, right ):
    return compare( left, '>', right )

def where( *args ):
    return { 'where' : args }

