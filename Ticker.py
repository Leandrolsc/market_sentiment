import yfinance as yfin
from pandas_datareader import data as web
import pandas as pd
import datetime
import sqlite3

connection = sqlite3.connect("test.db")
cursor = connection.cursor()


def CreateTableTicker():
    cursor.execute("""CREATE TABLE IF NOT EXISTS Ticker    
                (CodigoTicker INTEGER PRIMARY KEY
                    ,CodigoSetor INTEGER
                    ,CodigoInstituicao INTEGER
                    ,FOREIGN KEY(CodigoInstituicao) REFERENCES Instituicao(CodigoInstituicao)
                    ,FOREIGN KEY(CodigoSetor) REFERENCES Setor(CodigoSetor))""")
    

petr4 = yfin.Ticker("PETR4.SA")
petr4 = petr4.info

print(petr4['industry'])
print(petr4['sector'])
print(petr4['fullTimeEmployees'])
print(petr4['longName'])
print(petr4['lastDividendValue'])
print(petr4['website'])
print(petr4['enterprisevalue'])
print(petr4['recommendationMean'])