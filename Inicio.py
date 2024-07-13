import streamlit as st
import investpy as inv
from Ticker import Ticker
from Cotacoes import Cotacoes
from Noticias import Noticias
import datetime
import plotly.express as px


st.set_page_config(page_title="Inicio"
                    ,page_icon = "🏠"
                    ,layout= 'wide')


with st.container():
    st.title("InvestimentoInfoPy")
    st.write("---")


st.markdown('''
Informações sobre ações e analise de sentimento
            
Esse projeto tem como objetivo realizar um ETL dinamico através da ferramenta streamlit, que tem como objetivo a analise das cotações e noticias das ações na Bolsa de Valores do Brasil.

Para os dados de cotações será utilizado a API do Yahoo Finance(yfinance) sendo o meio mais prático de se conseguir cotações historicas na internet.

Para os dados de noticias foi realizado um webscrapping no Google News, utilizando a biblioteca BeautifulSoap4. 

Para a analise de sentimento foi utilizado a biblioteca LeIA para analisar as manchetes.

Os dados serão armazenados na memoria utilizando o sqllite.

## 🛠️ Foi Construído com

* [Draw.io](https://app.diagrams.net/?mode=google) - Aplicativo para a Modelagem das ER e Dimensional.
* [Visual Code](https://code.visualstudio.com/download) - IDE utilizada para construção dos Scripts em python.
* [Streamlit](https://docs.streamlit.io/) - IDE utilizada para construção dos Scripts em python.


Mais informações sobre o projeto no repositório:

''')
st.write("Repositorio: [Clique aqui](https://github.com/Leandrolsc/InvestimentoInfoPy)")

