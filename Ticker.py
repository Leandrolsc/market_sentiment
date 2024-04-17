import yfinance as yfin
from pandas_datareader import data as web
import pandas as pd
import sqlite3
import investpy as inv


connection = sqlite3.connect("InvestimentoInfoPy.db")
cursor = connection.cursor()

def CreateTableTicker():
    create_table =  """CREATE TABLE IF NOT EXISTS Ticker    
                (Ticker TEXT
                    ,Industry TEXT
                    ,Sector TEXT
                    ,fullTimeEmployees INTEGER
                    ,LongName TEXT
                    ,lastDividendValue DECIMAL
                    ,WebSite TEXT
                    ,EnterpriseValue DECIMAL
                    ,RecomendationMean DECIMAL
                   );"""
    cursor.execute(create_table)
    
def access_list():
    lista_tickers = inv.get_stocks_list("brazil")
    print(lista_tickers)

def pick_ticker():
    access_list()
    ticker = input()
    return ticker

def dataframe():
     return pd.DataFrame(columns=['Ticker','Industry','Sector','fullTimeEmployees','LongName','lastDividendValue','WebSite','EnterpriseValue','RecomendationMean'])

def get_ticker():
    ticker = pick_ticker()
    ticker_dict = yfin.Ticker(f"{ticker}.SA")
    ticker_dict = ticker_dict.info
    df = dataframe()
    ticker_list = {}
    ticker_list['Ticker'] = ticker
    ticker_list['Industry'] = ticker_dict['industry']
    ticker_list['Sector'] = ticker_dict['sector']
    ticker_list['fullTimeEmployees'] = ticker_dict['fullTimeEmployees']
    ticker_list['LongName'] = ticker_dict['longName']
    ticker_list['lastDividendValue'] = ticker_dict['lastDividendValue']
    ticker_list['WebSite'] = ticker_dict['website']
    ticker_list['EnterpriseValue'] = ticker_dict['enterpriseValue']
    ticker_list['RecomendationMean'] = ticker_dict['recommendationMean']
    ticker_list = pd.DataFrame(ticker_list, index=[0])
    df = pd.concat([df, ticker_list], ignore_index=True)
    return df


def Insert_ticker(df):
    CreateTableTicker()
    Ticker = str(df['Ticker'][0])
    Industry = str(df['Industry'][0])
    Sector = str(df['Sector'][0])
    fullTimeEmployees = int(df['fullTimeEmployees'].iloc[0])
    LongName = str(df['LongName'][0])
    lastDividendValue = float(df['lastDividendValue'].iloc[0])
    WebSite = str(df['WebSite'][0])
    EnterpriseValue = float(df['EnterpriseValue'].iloc[0])
    RecomendationMean = float(df['RecomendationMean'].iloc[0])
    insert = """INSERT INTO Ticker (Ticker
                                            ,Industry
                                            ,Sector
                                            ,fullTimeEmployees
                                            ,LongName
                                            ,lastDividendValue
                                            ,WebSite
                                            ,EnterpriseValue
                                            ,RecomendationMean)
                    VALUES(?
                            ,?
                            ,?
                            ,?
                            ,?
                            ,?
                            ,?
                            ,?
                            ,?);"""
    dados = (Ticker, Industry, Sector, fullTimeEmployees, LongName,lastDividendValue,WebSite,EnterpriseValue,RecomendationMean)
    cursor.execute(insert, dados)
    connection.commit()
    print('Ticker inserido com sucesso no Banco de Dados')
    cursor.close()

df = get_ticker()
Insert_ticker(df)