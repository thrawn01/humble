import os

db_file = ( "/tmp/%s.db" % os.getpid() )
employee_row1 = { 'first' : 'Derrick', 'last' : 'Wippler',
                  'age' : 31, 'address' : "DataPoint Drive" }
employee_row2 = { 'first' : 'Brandie', 'last' : 'Marie',
                  'age' : 28, 'address' : "HelloKitty Drive" }

table_name = 'employee'
table_create = """
    CREATE TABLE employee (
        first   CHAR(30),
        last    CHAR(30),
        age     INTEGER,
        address TEXT
    ); """

