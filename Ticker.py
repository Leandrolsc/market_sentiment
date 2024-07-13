import yfinance as yfin
import pandas as pd
import sqlite3
import datetime

class Ticker():
    def __init__(self,ticker_symbol):
        self.ticker_symbol = ticker_symbol  

    def CreateTableTicker(self):
        connection = sqlite3.connect("InvestimentoInfoPy.db")
        cursor = connection.cursor()
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
                        ,currentPrice DECIMAL
                    );"""
        cursor.execute(create_table)
        return print('Tabela Ticker criada com sucesso')



    def get_ticker(self,ticker_symbol):
        ticker = ticker_symbol
        ticker_dict = yfin.Ticker(f"{ticker}.SA")
        ticker_dict = ticker_dict.info
        df = pd.DataFrame(columns=['Ticker','Industry','Sector','fullTimeEmployees','LongName','lastDividendValue','WebSite','EnterpriseValue','RecomendationMean','currentPrice'])
        ticker_list = {}
        ticker_list['Ticker'] = ticker
        try:
            ticker_list['Industry'] = ticker_dict['industry'] 
        except KeyError:
            ticker_list['Industry'] = ''
        try:
            ticker_list['Sector'] = ticker_dict['sector']
        except KeyError:
            ticker_list['Sector'] = ''
        try:
            ticker_list['fullTimeEmployees'] = ticker_dict['fullTimeEmployees']  
        except KeyError:
            ticker_list['fullTimeEmployees'] = 0
        try:
            ticker_list['LongName'] = ticker_dict['longName']
        except KeyError:
            ticker_list['LongName'] = ''
        try:
            ticker_list['lastDividendValue'] = ticker_dict['lastDividendValue']
        except KeyError:
            ticker_list['lastDividendValue'] = 0
        try:
            ticker_list['WebSite'] = ticker_dict['website']
        except KeyError:
            ticker_list['WebSite'] = ''
        try:
            ticker_list['EnterpriseValue'] = ticker_dict['enterpriseValue']
        except KeyError:
            ticker_list['EnterpriseValue'] = 0
        try:
            ticker_list['RecomendationMean'] = ticker_dict['recommendationMean']
        except KeyError:
            ticker_list['RecomendationMean'] = 0
        try:
            ticker_list['currentPrice'] = ticker_dict['currentPrice']
        except KeyError:
            ticker_list['currentPrice'] = 0
        ticker_list = pd.DataFrame(ticker_list, index=[0])
        df = pd.concat([df, ticker_list], ignore_index=True)
        return df

    def truncate_table(self,ticker_symbol):
        connection = sqlite3.connect("InvestimentoInfoPy.db")
        cursor = connection.cursor()
        Ticker.CreateTableTicker(self)
        truncate = f"""DELETE FROM Ticker WHERE Ticker = '{ticker_symbol}'"""
        cursor.execute(truncate)
        connection.commit()
        cursor.close()

    def Insert_ticker(self,df):
        connection = sqlite3.connect("InvestimentoInfoPy.db")
        cursor = connection.cursor()
        Ticker.CreateTableTicker(self)
        df['Ticker'] = df['Ticker'].apply(lambda x:str(x) if x is not None else '')
        df['Industry'] = df['Industry'].apply(lambda x: str(x) if x is not None else '')
        df['Sector'] = df['Sector'].apply(lambda x: str(x) if x is not None else '')
        df['fullTimeEmployees'] = df['fullTimeEmployees'].apply(lambda x: int(x) if x is not None else 0)
        df['LongName'] = df['LongName'].apply(lambda x: str(x) if x is not None else '')
        df['lastDividendValue'] = df['lastDividendValue'].apply(lambda x: float(x) if x is not None else 0)
        df['WebSite'] = df['WebSite'].apply(lambda x: str(x) if x is not None else '')
        df['EnterpriseValue'] = df['EnterpriseValue'].apply(lambda x: float(x) if x is not None else 0)
        df['RecomendationMean'] = df['RecomendationMean'].apply(lambda x: float(x) if x is not None else 0)
        df['currentPrice'] = df['currentPrice'].apply(lambda x: float(x) if x is not None else 0)


        insert = """INSERT INTO Ticker (Ticker
                                                ,Industry
                                                ,Sector
                                                ,fullTimeEmployees
                                                ,LongName
                                                ,lastDividendValue
                                                ,WebSite
                                                ,EnterpriseValue
                                                ,RecomendationMean
                                                ,currentPrice)
                        VALUES(?
                                ,?
                                ,?
                                ,?
                                ,?
                                ,?
                                ,?
                                ,?
                                ,?
                                ,?);"""
        dados = (df.values.tolist())
        cursor.executemany(insert, dados)
        connection.commit()
        print('Ticker inserido com sucesso no Banco de Dados')
        cursor.close()


    def processo_completo(self,ticker_symbol):
        connection = sqlite3.connect("InvestimentoInfoPy.db")
        cursor = connection.cursor()
        df = Ticker.get_ticker(self,ticker_symbol)
        Ticker.truncate_table(self,ticker_symbol)
        Ticker.Insert_ticker(self,df)
        select = f"""SELECT * FROM Ticker WHERE Ticker = '{ticker_symbol}'"""
        cursor.execute(select)
        rows = cursor.fetchall()
        connection.commit()
        cursor.close()
     
        ticker_table = pd.DataFrame(rows,columns=['Ticker','Industry','Sector','fullTimeEmployees','LongName','lastDividendValue','WebSite','EnterpriseValue','RecomendationMean','currentPrice'])

        return ticker_table
    
    def consulta_ticker():
        connection = sqlite3.connect("InvestimentoInfoPy.db")
        cursor = connection.cursor()
        select = f"""SELECT * FROM Ticker"""
        cursor.execute(select)
        rows = cursor.fetchall()
        connection.commit()
        cursor.close()
     
        ticker_table = pd.DataFrame(rows,columns=['Ticker','Industry','Sector','fullTimeEmployees','LongName','lastDividendValue','WebSite','EnterpriseValue','RecomendationMean','currentPrice'])

        return ticker_table


#info = Ticker.processo_completo(Ticker,ticker_symbol=option)
#print(info)