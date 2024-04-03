from requests_html import HTMLSession
from bs4 import BeautifulSoup
import pandas as pd
import datetime


def getnews(ticker):
    acesso = HTMLSession()
    datacoleta = datetime.date.today()
    link = acesso.get(f'https://news.google.com/search?q={ticker}&hl=pt-BR&gl=BR&ceid=BR%3Apt-419')
    html = BeautifulSoup(link.text, 'lxml')
    valor = html.find_all('a', {'class':'JtKRv'})
    news = pd.DataFrame(columns=['Noticias','Ticker','DataColeta'])
    for i in valor:
        frase = i.text
        frase = (frase,f'{ticker}',datacoleta)
        getnews = pd.DataFrame([frase],columns=['Noticias','Ticker','DataColeta'])
        news = pd.concat([news, getnews], ignore_index=True) 
    return news


print(getnews('PETR4'))

