import streamlit as st
from streamlit_option_menu import option_menu
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from presentations.pages import inicio, metricas, tabelas

st.set_page_config(page_title="Inicio"
                    ,page_icon = "🏠"
                    ,layout= 'wide')



with st.sidebar:
    escolha = option_menu(
        "",
        ["Inicio", 
         "Métricas", 
         "Tabelas para Download"
         ],
        icons=['', 
               'bar-chart', 
               'gear',
               ],
        menu_icon="cast",
        default_index=0
    )

if escolha == "Tabelas para Download":
    tabelas.exibir()
elif escolha == "Métricas":
    metricas.exibir()
elif escolha == "Inicio":
    inicio.exibir()

    st.title("🏠 Introdução")
    st.markdown("---")

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

st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; font-size: 0.95em;'>
        Desenvolvido por: 
        <a href='https://www.linkedin.com/in/leandro-victor-silva-8a319b228/' target='_blank'><b>Leandro Victor Silva</b></a> e 
        Repositório do projeto: 
        <a href='https://github.com/Leandrolsc/market_sentiment' target='_blank'>
           <b>GitHub - Leandrolsc/PosTech_DataAnalytics_Datathon</b>
        </a>
    </div>
    """,
    unsafe_allow_html=True
)

