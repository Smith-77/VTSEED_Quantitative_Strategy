from psycopg2 import *

class DatabaseConnector:

    # def __init__(self, database: str, user="postgres", password="", host="127.0.0.1", port="5432"):
    def __init__(self, database: str, user="postgres", password="postgres", host="127.0.0.1", port="5432"):
        self._user = user
        self._password = password
        self._host = host
        self._port = port
        self._database = database
        
    def _create_connection(self):
        """
        Returns connection to an existing database or
        None if some error occurs
        """
        conn = None
        try:
            conn = connect(user=self._user,
                           password=self._password,
                           host=self._host,
                           port=self._port,
                           database=self._database)
        except Error as e:
            print(e)
        return conn

    def execute(self, statement, commit=False, fetch=None, params=None):
        """ Execute SQL statement and return the results
        """
        conn = self._create_connection()
        cursor = conn.cursor()
        toReturn = None
        try:
            if params:   
                cursor.execute(statement, params)
            else:
                cursor.execute(statement)

            toReturn = None
            if fetch == 'all':
                toReturn = cursor.fetchall()
            elif fetch == 'one':
                toReturn =  cursor.fetchone()
            elif fetch == 'many':
                toReturn = cursor.fetchmany()

            if commit:
                conn.commit()
                
        except Error as e:
            print(e)
            toReturn = None

        cursor.close()
        conn.close()
        return toReturn

    def _get_postgreSQL_details(self):
        conn = self._create_connection()
        return conn.get_dsn_parameters()

    def get_postgreSQL_version(self):
        return self.execute("SELECT version();", 'one')[0]

    '''

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
        '''


        

        