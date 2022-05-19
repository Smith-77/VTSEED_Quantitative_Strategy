CREATE TABLE gics_enum (
    id SERIAL PRIMARY KEY NOT NULL,
    industry TEXT NOT NULL,
    stoploss float8 NOT NULL
);

INSERT INTO gics_enum (industry) VALUES 
    ('healthcare'),
    ('consumer staples'),
    ('communication');

CREATE TABLE [IF NOT EXISTS] stocks (
   ticker VARCHAR ( 15 ) PRIMARY KEY NOT NULL,
   gics_industry INTEGER REFERENCES gics_enum (industry) ON UPDATE CASCADE NOT NULL
);

CREATE TABLE [IF NOT EXISTS] time_data (
    id SERIAL PRIMARY KEY NOT NULL
    jhk TIMESTAMP NOT NULL,
    ticker VARCHAR (15) REFERENCES stocks (ticker) ON UPDATE CASCADE NOT NULL,
    opening float8 NOT NULL,
    closing float8 NOT NULL,
);