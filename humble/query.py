""" 
    Defines the functions that create
    the query structure humble consumes
"""
__all__ = [ 'equal', 'lessThan', 'greaterThan', 'column', 'where' ]

def compare( left, operator, right ):
    return ( left, operator, right )

def equal( left, right ):
    return compare( left, '=', right )

def lessThan( left, right ):
    return compare( left, '<', right )

def greaterThan( left, right ):
    return compare( left, '>', right )

def column( table, column=None ):
    if column:
        return { 'column' : (table,column) }
    return { 'column' : (None,table) }

def where( *args ):
    return { 'where' : args }

