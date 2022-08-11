import sqlite3
from sqlite3 import Error
import pandas as pd
import sqlalchemy as sa
import datetime

class DatabaseConnector:

    def __init__(self, database_path):
            self._path_to_database = database_path
        
    def _create_connection(self):
        """ create a database connection to the SQLite database
            specified by db_file
        :param db_file: database file
        :return: Connection object or None
        """
        conn = None
        try:
            conn = sqlite3.connect(self._path_to_database,
                                detect_types=sqlite3.PARSE_DECLTYPES |
                                    sqlite3.PARSE_COLNAMES)
        except Error as e:
            print("************************************************************************************")
            print(e)

        return conn

    def _get_all_tables(self, conn):
        cur = conn.cursor()
        cur.execute("""
            SELECT name FROM sqlite_master WHERE type='table';
        """)
        tables = cur.fetchall()
        cur.close()
        return tables

    def _delete_table(self, conn, table_name: str):
        cur = conn.cursor()
        sql = "DROP TABLE IF EXISTS {table_name}".format(table_name = table_name)
        cur.execute(sql)
        cur.execute("VACUUM;")
        cur.close()

    def delete_all_tables(self):
        conn = self._create_connection()
        tables = self._get_all_tables(conn)
        for table in tables:
            print(table[0])
            self._delete_table(conn, table[0])
        conn.close()

    def get_column_names(self, table_name): 
        conn = self._create_connection()
        statement = "SELECT * FROM {table_name}".format(table_name = table_name) # COMMAND COMPOISITION WITH STRINGS IS BAD PRACTICE, UNSAFE TO SQL INJECTION ATTACKS!
        cursor = conn.execute(statement)
        names = list(map(lambda x: x[0], cursor.description))
        conn.close()
        return names

    def get_column_dtypes(self, table_name):
        conn = self._create_connection()
        sqlStatement = "SELECT name, type FROM pragma_table_info('{table_name}');".format(table_name = table_name)
        results =  conn.execute(sqlStatement).fetchall()
        conn.close()
        return results

    def load_csv_into_sql_table(self, src_file_name, table_name, dtype=None, if_exists='append', index=False, cleaning_function=None):
        # Load pandas DF from csv
        df = pd.read_csv(src_file_name)

        # Perform data cleaning
        if cleaning_function:
            df = cleaning_function(df)
            
        conn = self._create_connection()
        # Convert pandas DF into an SQL table
        try:
            df.to_sql(table_name,
            conn,
            if_exists=if_exists,
            index=index,
            dtype=dtype)
        except Exception as e:
            print("Ruh roh, Shaggy! An error has occured: ", e.__class__)

        conn.close()

    def get_database_path(self):
        return self._path_to_database

    def execute(self, statement, fetch: str, params=None):
        conn = self._create_connection()
        # TODO: Try Except
        results = None
        if params:   
            results = conn.execute(statement, params)
        else:
            results = conn.execute(statement)

        toReturn = None
        if fetch == 'all':
            toReturn = results.fetchall()
        elif fetch == 'one':
            toReturn =  results.fetchone()
        
        conn.close()
        return toReturn


        

        