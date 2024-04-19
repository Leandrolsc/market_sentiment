import yfinance as yfin
import pandas as pd
import sqlite3

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
                    );"""
        cursor.execute(create_table)


    def get_ticker(self,ticker_symbol):
        ticker = ticker_symbol
        ticker_dict = yfin.Ticker(f"{ticker}.SA")
        ticker_dict = ticker_dict.info
        df = pd.DataFrame(columns=['Ticker','Industry','Sector','fullTimeEmployees','LongName','lastDividendValue','WebSite','EnterpriseValue','RecomendationMean'])
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
        ticker_list = pd.DataFrame(ticker_list, index=[0])
        df = pd.concat([df, ticker_list], ignore_index=True)
        return df


    def Insert_ticker(self,df):
        connection = sqlite3.connect("InvestimentoInfoPy.db")
        cursor = connection.cursor()
        Ticker.CreateTableTicker(self)
        ticker = str(df['Ticker'][0])

        if df['Industry'][0] is not None:
            Industry = str(df['Industry'][0])
        else:
            Industry = ''

        if df['Sector'][0] is not None:
            Sector = str(df['Sector'][0])
        else:
            Sector = ''

        if df['fullTimeEmployees'].iloc[0] is not None:
            fullTimeEmployees = int(df['fullTimeEmployees'].iloc[0])
        else:
            fullTimeEmployees = 0

        if df['LongName'][0] is not None:
            LongName = str(df['LongName'][0])
        else:
            LongName = ''
        
        if df['lastDividendValue'].iloc[0] is not None:
            lastDividendValue = float(df['lastDividendValue'].iloc[0])
        else:
            lastDividendValue = 0
        
        if df['WebSite'][0] is not None:
            WebSite = str(df['WebSite'][0])
        else:
            WebSite = ''

        if df['EnterpriseValue'].iloc[0] is not None:
            EnterpriseValue = float(df['EnterpriseValue'].iloc[0])
        else:
            EnterpriseValue = ''

        if df['RecomendationMean'].iloc[0] is not None:
            RecomendationMean = float(df['RecomendationMean'].iloc[0])
        else:
            RecomendationMean = 0

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
        dados = (ticker, Industry, Sector, fullTimeEmployees, LongName,lastDividendValue,WebSite,EnterpriseValue,RecomendationMean)
        cursor.execute(insert, dados)
        connection.commit()
        print('Ticker inserido com sucesso no Banco de Dados')
        cursor.close()


    def processo_completo(self,ticker_symbol):
        connection = sqlite3.connect("InvestimentoInfoPy.db")
        cursor = connection.cursor()
        df = Ticker.get_ticker(self,ticker_symbol)
        Ticker.Insert_ticker(self,df)
        select = """SELECT * FROM Ticker"""
        cursor.execute(select)
        rows = cursor.fetchall()

        for row in rows:
            info = row
        return info



#info = Ticker.processo_completo(Ticker,ticker_symbol=option)
#print(info)