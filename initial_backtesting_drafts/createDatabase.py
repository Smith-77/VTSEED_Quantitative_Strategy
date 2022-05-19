import sqlite3

con = sqlite3.connect('SEED.db')
cur = con.cursor()

# Create new databasepy
cur.execute('''DROP TABLE IF EXISTS gics_enum''')

cur.execute('''CREATE TABLE gics_enum (
    id SERIAL PRIMARY KEY,
    industry TEXT UNIQUE NOT NULL,
    stoploss float8 NOT NULL)''')

cur.execute('''INSERT INTO gics_enum (industry, stoploss) VALUES
    ("healthcare", .1),
    ("consumer discretionary", .1),
    ("communications", .2)''')

cur.execute('''CREATE TABLE IF NOT EXISTS stocks (
    ticker VARCHAR(15) PRIMARY KEY NOT NULL,
    gics_industry TEXT REFERENCES gics_enum (industry) ON UPDATE CASCADE NOT NULL)''')

cur.execute('''CREATE TABLE IF NOT EXISTS time_data (
    id SERIAL PRIMARY KEY,
    date TIMESTAMP NOT NULL,
    ticker VARCHAR(15) REFERENCES stocks (ticker) ON UPDATE CASCADE NOT NULL,
    opening float8 NOT NULL,
    closing float8 NOT NULL)''')

# Save and close the changes
con.commit()
con.close()