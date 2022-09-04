import sqlite3
from sqlite3 import Error
import pandas as pd
import sqlalchemy as sa
import datetime

'''
UTILITY FUNCTIONS___________________________________________________________________
    creat_connection
    delete_all_tables
    get_tables
    delete_table
    get_column_names
    get_column_dtypes
    load_csv_into_sql_table
'''
def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file,
                               detect_types=sqlite3.PARSE_DECLTYPES |
                                sqlite3.PARSE_COLNAMES)
    except Error as e:
        print(e)

    return conn

def delete_all_tables(conn):
    tables = get_all_tables(conn)
    for table in tables:
        print(table[0])
        delete_table(conn, table[0])

def get_all_tables(conn):
    cur = conn.cursor()
    cur.execute("""
        SELECT name FROM sqlite_master WHERE type='table';
    """)
    tables = cur.fetchall()
    cur.close()
    return tables

def delete_table(conn, table_name: str):
    cur = conn.cursor()
    sql = "DROP TABLE IF EXISTS {table_name}".format(table_name = table_name)
    cur.execute(sql)
    cur.execute("VACUUM;")
    cur.close()

def get_column_names(conn, table_name): 
    statement = "SELECT * FROM {table_name}".format(table_name = table_name) # COMMAND COMPOISITION WITH STRINGS IS BAD PRACTICE, UNSAFE TO SQL INJECTION ATTACKS!
    cursor = conn.execute(statement)
    names = list(map(lambda x: x[0], cursor.description))
    return names

def get_column_dtypes(conn, table_name):
    sqlStatement = "SELECT name, type FROM pragma_table_info('{table_name}');".format(table_name = table_name)
    return conn.execute(sqlStatement).fetchall()

def load_csv_into_sql_table(conn, src_file_name, table_name, dtype=None, if_exists='append', index=False, cleaning_function=None):
    # Load pandas DF from csv
    df = pd.read_csv(src_file_name)

    # Perform data cleaning
    if cleaning_function:
        df = cleaning_function(df)
        
    # Convert pandas DF into an SQL table
    try:
        df.to_sql(table_name,
        conn,
        if_exists=if_exists,
        index=index,
        dtype=dtype)
    except Exception as e:
        print("Ruh roh, Shaggy! An error has occured: ", e.__class__)