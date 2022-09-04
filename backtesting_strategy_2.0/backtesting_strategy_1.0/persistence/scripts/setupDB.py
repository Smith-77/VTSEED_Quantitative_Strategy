import sqlite3
from sqlite3 import Error
import pandas as pd
import sqlalchemy as sa
import datetime
import os

# from persistence.scripts.sqlite3_util import *


'''
SCRIPTS ___________________________________________________________________
'''

def setup_test_db():
    path = os.path
    database = "./persistence/databases/test_data.db"
    # database = r"" + os.path.dirname(os.path.abspath(__file__)) + "\\..\\databases\\test_data.db"
    print(database)

    # create a database connection
    conn = create_connection(database)
    with conn:
        # Drop all existing tables/data
        delete_all_tables(conn)

        # Load S&P time data
        table_name = 'time_data'
        data_types = {'Date': 'Date',
                      'Ticker': 'Text',
                      'Price': 'Float'
                     }
        load_csv_into_sql_table(conn, os.path.dirname(os.path.abspath(__file__)) + '../data/SP500_Test_Small_Time_1.0.csv', table_name=table_name, dtype=data_types, cleaning_function=_time_data_cleaning)
        print(get_column_dtypes(conn, table_name))
        
def _time_data_cleaning(df: pd.DataFrame):
    df['Date'] = df['Date'].apply(lambda date: datetime.datetime.strptime(date, '%m/%d/%Y').date())
    return df

"""
def main():
    database = r"./example.db"

    # create a database connection
    conn = create_connection(database)
    with conn:
        # Set Up Tables
        # set_up_tables(conn)

        # Load S&P Data
        load_csv_into_sql_table(conn, '../data/SP500_Test_Small_Time_1.0.csv', 'time_data')

        # print(get_column_names(conn, 'time_data'))

        print("*************************************************************************************")
        # print(get_column_dtypes(conn, 'time_data'))

        conn.execute("INSERT INTO time_data(date, ticker) VALUES(?, ?)", (datetime.date(2022, 2, 1), 'deleteThis'))
        results = conn.execute("SELECT Date FROM time_data WHERE Date = ?", [(datetime.date(2022, 1, 5))]).fetchall()
        for result in results:
            print(type(result[0]))
            print(result)

        # Delete all Tables
        # delete_all_tables(conn)
"""



if __name__ == '__main__':
    # main()
    setup_test_db()