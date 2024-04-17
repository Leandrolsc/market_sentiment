from requests_html import HTMLSession
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import sqlite3
from LeIA import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()


connection = sqlite3.connect("InvestimentoInfoPy.db")
cursor = connection.cursor()

def analyze_sentiment(noticia):
    '''Função que recebe um texto como entrada, analisa seu sentimento e interpreta o resultado'''
    sentiment = analyzer.polarity_scores(noticia)
    compound_score = sentiment['compound']
    if compound_score >= 0.05:
        return "1"
    elif compound_score <= -0.05:
        return "-1"
    else:
        return "0"

     

def CreateTableNoticia():
    cursor.execute("""CREATE TABLE IF NOT EXISTS Noticia   
                (CodigoNoticia INTEGER PRIMARY KEY
                    ,CodigoTicker INTEGER
                    ,CodigoInstituicao INTEGER
                    ,FOREIGN KEY(CodigoTicker) REFERENCES Ticker(CodigoTicker)
                   )""")
    

def getnews(ticker):
    acesso = HTMLSession()
    datacoleta = datetime.date.today()
    link = acesso.get(f'https://news.google.com/search?q={ticker}&hl=pt-BR&gl=BR&ceid=BR%3Apt-419')
    html = BeautifulSoup(link.text, 'lxml')
    valor = html.find_all('a', {'class':'JtKRv'})
    news = pd.DataFrame(columns=['Noticias','Ticker','Sentimento','DataColeta'])
    for i in valor:
        noticia = i.text
        noticia = (noticia,f'{ticker}',analyze_sentiment(noticia),datacoleta)
        getnews = pd.DataFrame([noticia],columns=['Noticias','Ticker','Sentimento','DataColeta'])
        news = pd.concat([news, getnews], ignore_index=True) 
    return news


print(getnews('PETR4'))

