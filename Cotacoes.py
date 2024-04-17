import yfinance as yfin
from pandas_datareader import data as web
import pandas as pd
import datetime
import sqlite3

connection = sqlite3.connect("InvestimentoInfoPy.db")
cursor = connection.cursor()


def CreateTableCotacao():
    cursor.execute("""CREATE TABLE IF NOT EXISTS Cotacao
                (Ticker TEXT
                    ,Open DECIMAL
                    ,High DECIMAL
                    ,Low DECIMAL
                    ,Close DECIMAL
                    ,Adj Close DECIMAL
                    ,Volume INT
                    ,Data DATE
                    ,Variacao DECIMAL
                    ,DataColeta DATETIME
                   );""")


def dataframe():
     return pd.DataFrame(columns=['Open','High','Low','Close','Adj Close','Volume','Data','Variacao','DataColeta'])

#Arredondar Adj Close

def Acao(ticker):
    ontem = datetime.date.today() - datetime.timedelta(days=1)
    hoje = datetime.date.today()
    yfin.pdr_override()
    df = dataframe()
    cotacao = web.get_data_yahoo(f'{ticker}.SA',start='2024-03-01',end=ontem)
    cotacao['Data'] = cotacao.index
    cotacao['Data'] = cotacao['Data'].dt.tz_localize(None)
    cotacao['Variacao'] = (cotacao['High']  - cotacao['Low']) / cotacao['Low']  * 100 
    cotacao['DataColeta'] = hoje
    df = pd.concat([df, cotacao], ignore_index=True)
    return df



Dados = Acao('Acao','RAIZ4')

print(Dados)






#Noticias do yahoo finance

#Analise de sentimento