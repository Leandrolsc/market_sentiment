from requests_html import HTMLSession
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import sqlite3
# Novos imports necessários
from textblob import TextBlob

class Noticias():
    def __init__(self, ticker_symbol):
        # Corrigi um pequeno erro de digitação de 'symbil' para 'symbol'
        self.ticker_symbol = ticker_symbol
        # Carrega o modelo de análise de sentimento APENAS UMA VEZ.
        # Isso economiza muito tempo e memória.

    def analyze_sentiment(noticia):
        '''
        Função que analisa o sentimento usando TextBlob-PT.
        '''
        # Cria um objeto TextBlob
        blob = TextBlob(noticia)
        
        # O atributo .sentiment.polarity retorna um valor entre -1.0 e 1.0
        compound_score = blob.sentiment.polarity

        if compound_score >= 0.05:
            return "1"
        elif compound_score <= -0.05:
            return "-1"
        else:
            return "0"

    def CreateTableNoticia():
        connection = sqlite3.connect("InvestimentoInfoPy.db")
        cursor = connection.cursor()
        create_table = """CREATE TABLE IF NOT EXISTS Noticia   
                    (Noticia TEXT
                        ,Ticker TEXT
                        ,Sentimento INTEGER
                        ,DataColeta DATE
                    )"""
        cursor.execute(create_table)
        return print ("Tabela Noticias criada com sucesso")

    def get_news(ticker_symbol):
        acesso = HTMLSession()
        datacoleta = datetime.date.today()
        link = acesso.get(f'https://news.google.com/search?q={ticker_symbol}&hl=pt-BR&gl=BR&ceid=BR%3Apt-419')
        html = BeautifulSoup(link.text, 'lxml')
        valor = html.find_all('a', {'class':'JtKRv'})
        news = pd.DataFrame(columns=['Noticia','Ticker','Sentimento','DataColeta'])
        for i in valor:
            noticia = i.text
            noticia = (noticia,f'{ticker_symbol}',Noticias.analyze_sentiment(noticia),datacoleta)
            getnews = pd.DataFrame([noticia],columns=['Noticia','Ticker','Sentimento','DataColeta'])
            news = pd.concat([news, getnews], ignore_index=True) 
        return news

    def truncate_table(ticker_symbol):
        connection = sqlite3.connect("InvestimentoInfoPy.db")
        cursor = connection.cursor()
        Noticias.CreateTableNoticia()
        truncate = f"""DELETE FROM Noticia WHERE Ticker = '{ticker_symbol}'"""
        cursor.execute(truncate)
        connection.commit()
        cursor.close()

    def Insert_Noticias(df):
        connection = sqlite3.connect("InvestimentoInfoPy.db")
        cursor = connection.cursor()
        Noticias.CreateTableNoticia()
        df['Noticia'] = df['Noticia'].apply(lambda x: str(x) if x is not None else '')
        df['Ticker'] = df['Ticker'].apply(lambda x: str(x) if x is not None else '')
        df['Sentimento'] = df['Sentimento'].apply(lambda x: int(x) if x is not None else 0)
        df['DataColeta'] = df['DataColeta'].apply(lambda x: str(x) if x is not None else '')

        insert = """INSERT INTO Noticia (Noticia
                                            ,Ticker
                                            ,Sentimento
                                            ,DataColeta)
                    VALUES (?
                            ,?
                            ,?
                            ,?);"""
        dados = (df.values.tolist())
        cursor.executemany(insert, dados)
        connection.commit()
        print('Noticias inseridas com sucessso no Banco de Dados')
        cursor.close()

    def processo_completo(ticker_symbol):
        connection = sqlite3.connect("InvestimentoInfoPy.db")
        cursor = connection.cursor()
        df = Noticias.get_news(ticker_symbol)
        Noticias.truncate_table(ticker_symbol)
        Noticias.Insert_Noticias(df)
        select = f"""SELECT * FROM Noticia where Ticker = '{ticker_symbol}'"""
        cursor.execute(select)
        rows = cursor.fetchall()
        connection.commit()
        cursor.close()

        news_table = pd.DataFrame(rows,columns=['Noticia','Ticker','Sentimento','DataColeta'])
        
        return news_table
    
    def consulta_noticias():
        connection = sqlite3.connect("InvestimentoInfoPy.db")
        cursor = connection.cursor()
        select = f"""SELECT * FROM Noticia"""
        cursor.execute(select)
        rows = cursor.fetchall()
        connection.commit()
        cursor.close()

        news_table = pd.DataFrame(rows,columns=['Noticia','Ticker','Sentimento','DataColeta'])
        
        return news_table
    

    def consulta_noticias_negativas(tikcer_symbol):
        connection = sqlite3.connect("InvestimentoInfoPy.db")
        cursor = connection.cursor()
        select = f"""SELECT Noticia 
                        FROM Noticia 
                        WHERE Sentimento = -1 
                        AND Ticker = '{tikcer_symbol}'
                        LIMIT 3"""
        cursor.execute(select)
        rows = cursor.fetchall()
        connection.commit()
        cursor.close()

        news_table = pd.DataFrame(rows,columns=['Noticia'])
        
        return news_table
    