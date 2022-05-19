import sqlite3
import pandas as pd

con = sqlite3.connect('SEED.db')
cur = con.cursor()

def getAllStockTickers():
    stockTickers = con.execute('''SELECT ticker from stocks''')
    cols = [column[0] for column in stockTickers.description]
    results = pd.DataFrame.from_records(data = stockTickers.fetchall(), columns = cols)
    return results

print(getAllStockTickers())

con.execute('''INSERT into stocks (ticker, gics_industry) VALUES
    ("ZIM", "communications")''')

con.commit()

print(getAllStockTickers())

con.close()