# InvestimentoInfoPy

Este projeto tem como objetivo realizar um ETL dinâmico através da ferramenta Streamlit, com o propósito de analisar as cotações e notícias das ações na Bolsa de Valores do Brasil.

Para os dados de cotações, será utilizada a API do Yahoo Finance (yfinance), sendo o meio mais prático de obter cotações históricas na internet.

Para os dados de notícias, foi realizado um web scraping no Google News, utilizando a biblioteca BeautifulSoup4.

Para a análise de sentimento, foi utilizada a biblioteca LeIA para analisar as manchetes.

Os dados serão armazenados na memória utilizando o SQLite.

## 🛠️ Foi Construído com

* [Draw.io](https://app.diagrams.net/?mode=google) - Aplicativo para a Modelagem das ER e Dimensional.
* [Visual Code](https://code.visualstudio.com/download) - IDE utilizada para construção dos Scripts em python.
* [Streamlit](https://docs.streamlit.io/) - IDE utilizada para construção dos Scripts em python.



## Para execução será necessário

# Instalar as bibliotecas: 
    `pip install streamlit sqlite bs4 pandas pandas_datareader datetime plotly requests_html LeIA`

# Execução do streamlit:
    Basta executar no terminal o comando `streamlit run Inicio.py` que o streamlit vai iniciar.