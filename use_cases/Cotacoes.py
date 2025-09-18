import yfinance as yfin
from pandas_datareader import data as web
import pandas as pd
import datetime
import sqlite3

class Cotacoes():
    def __init__(self,ticker_symbol,inicio,fim):
        self.ticker_symbol = ticker_symbol  
        self.inicio = inicio
        self.fim = fim


    def CreateTableCotacao(self):
        connection = sqlite3.connect("InvestimentoInfoPy.db")
        cursor = connection.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS Cotacao
                    (Ticker TEXT
                        ,Date DATE
                        ,Open DECIMAL
                        ,High DECIMAL
                        ,Low DECIMAL
                        ,Close DECIMAL
                        ,Volume INT          
                        ,Dividends DECIMAL           
                        ,'Stock Splits' DECIMAL
                        ,DataColeta DATETIME
                    );""")       
        return print('Tabela Cotacao criada com sucesso')


    def Acao(self,ticker_symbol,inicio,fim):
        hoje = datetime.date.today()
        #yfin.pdr_override()
        ticker_search = yfin.Ticker(f'{ticker_symbol}.SA')
        df = pd.DataFrame(columns=['Ticker','Date','Open','High','Low','Close','Volume','Dividends','Stock Splits','DataColeta'])
        cotacao = ticker_search.history(start=inicio,end=fim)
        cotacao['Date'] = cotacao.index
        #cotacao['Date'] = cotacao['Date'].dt.tz_localize(None)
        cotacao['DataColeta'] = hoje
        cotacao['Ticker'] = ticker_symbol
        df = pd.concat([df,cotacao], ignore_index=True)
        return df

    def Insert_cotacao(self,df):
        connection = sqlite3.connect("InvestimentoInfoPy.db")
        cursor = connection.cursor()
        Cotacoes.CreateTableCotacao(self)            
        decimals = 2
        df['Ticker'] = df['Ticker'].apply(lambda x: str(x) if x is not None else '')
        df['Date'] = df['Date'].apply(lambda x: x.strftime("%Y-%m-%d") if x is not None else '')
        df['Open'] = df['Open'].apply(lambda x: round(float(x), decimals) if x is not None else 0)
        df['High'] = df['High'].apply(lambda x: round(float(x), decimals) if x is not None else 0)
        df['Low'] = df['Low'].apply(lambda x: round(float(x), decimals) if x is not None else 0)
        df['Close'] = df['Close'].apply(lambda x: round(float(x), decimals) if x is not None else 0)
        df['Volume'] = df['Volume'].apply(lambda x: int(x) if x is not None else 0)
        df['Dividends'] = df['Dividends'].apply(lambda x: round(float(x), decimals) if x is not None else 0)
        df['Stock Splits'] = df['Stock Splits'].apply(lambda x: round(float(x), decimals) if x is not None else 0)
        df['DataColeta'] = df['DataColeta'].apply(lambda x: str(x) if x is not None else '')
        insert = """INSERT INTO Cotacao (Ticker
                                            ,Date
                                            ,Open
                                            ,High
                                            ,Low
                                            ,Close
                                            ,Volume   
                                            ,Dividends                                      
                                            ,'Stock Splits'
                                            ,DataColeta)
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
        dados = df.values.tolist() 
        cursor.executemany(insert, dados)
        connection.commit()
        print('Cotacoes inseridas com sucesso no Banco de Dados')
        cursor.close()

    def truncate_table(self,ticker_symbol):
        connection = sqlite3.connect("InvestimentoInfoPy.db")
        cursor = connection.cursor()
        Cotacoes.CreateTableCotacao(self)
        truncate = f"""DELETE FROM Cotacao WHERE Ticker = '{ticker_symbol}'"""
        cursor.execute(truncate)
        connection.commit()
        cursor.close()

    def processo_completo(self,ticker_symbol,inicio,fim):
        connection = sqlite3.connect("InvestimentoInfoPy.db")
        cursor = connection.cursor()
        df = Cotacoes.Acao(self,ticker_symbol,inicio,fim)
        Cotacoes.truncate_table(self,ticker_symbol)
        Cotacoes.Insert_cotacao(self,df)
        select = f"""SELECT * FROM Cotacao WHERE Ticker = '{ticker_symbol}'"""
        cursor.execute(select)
        rows = cursor.fetchall()
        connection.commit()
        cursor.close()

        cotacao_table = pd.DataFrame(rows,columns=['Ticker','Date','Open','High','Low','Close','Volume','Dividends','Stock Splits','DataColeta'])


        return cotacao_table    
    
    def consulta_cotacoes():
        connection = sqlite3.connect("InvestimentoInfoPy.db")
        cursor = connection.cursor()
        select = f"""SELECT * FROM Cotacao"""
        cursor.execute(select)
        rows = cursor.fetchall()
        connection.commit()
        cursor.close()

        cotacao_table = pd.DataFrame(rows,columns=['Ticker','Date','Open','High','Low','Close','Volume','Dividends','Stock Splits','DataColeta'])

        return cotacao_table 



