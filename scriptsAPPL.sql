CREATE TABLE appl (
    Date DATE,
    Open NUMERIC(10, 6),
    High NUMERIC(10, 6),
    Low NUMERIC(10, 6),
    Close NUMERIC(10, 6),
    Adj_Close NUMERIC(10, 6),
    Volume BIGINT
);

COPY appl from "C:\Users\EQUIPO\Downloads\archive\AAPL.csv" DELIMITER ',' CSV HEADER

Select * from appl

