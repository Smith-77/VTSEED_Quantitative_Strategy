import DatabaseConnector as dbc
from psycopg2 import sql
import datetime

dbConn = dbc.DatabaseConnector('seed')

query = sql.SQL("""SELECT Date, Ticker, Price FROM
                            (SELECT * FROM {table_name} WHERE Date =%s) as dated_info
                        WHERE FCF_TTM > %s ORDER BY NET_INCOME_TTM DESC LIMIT {limit}""").format(
                            table_name=sql.Identifier('test_data'),
                            limit=sql.Literal(3)
                        )
current_date = datetime.date(2022, 1, 1)
rawResults = dbConn.execute(query, fetch='all', params=[current_date, 50])
print(rawResults)