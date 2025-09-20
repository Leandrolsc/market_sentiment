# Market Sentiment

Este projeto realiza análise de ações brasileiras e sentimento de mercado por meio de um ETL dinâmico com [Streamlit](https://docs.streamlit.io/). O objetivo é coletar, armazenar e apresentar cotações históricas e notícias relevantes, fornecendo insights para investidores.

## Funcionalidades

- **Coleta de Cotações:** Utiliza a API do Yahoo Finance ([yfinance](https://pypi.org/project/yfinance/)) para buscar dados históricos de ações da B3.
- **Web Scraping de Notícias:** Realiza scraping no Google News com [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/) para coletar manchetes relacionadas aos tickers.
- **Análise de Sentimento:** Aplica a biblioteca [TextBlob](https://pypi.org/project/textblob/) para classificar o sentimento das notícias (positivo, negativo ou neutro).
- **Armazenamento Local:** Todos os dados são persistidos em um banco SQLite.
- **Dashboard Interativo:** Visualização dos dados, métricas, gráficos e download das tabelas em CSV via Streamlit.
- **Modelagem ER:** Imagem da modelagem do banco disponível em `arquivos/model/Primeria Modelagem ER.png`.
- **Download de Dados:** Exportação dos dados de tickers, cotações e notícias diretamente pelo dashboard.

## Estrutura do Projeto

```
market_sentiment/
├── .gitignore
├── InvestimentoInfoPy.db
├── readme.md
├── requirements.txt
├── .streamlit/
│   └── config.toml
├── arquivos/
│   └── model/
│       └── Primeria Modelagem ER.png
├── presentations/
│   ├── app.py
│   └── custom_pages/
│       ├── metricas.py
│       └── tabelas.py
└── use_cases/
    ├── Cotacoes.py
    ├── Noticias.py
    └── Ticker.py
```

## Tecnologias Utilizadas

- [Python 3](https://www.python.org/)
- [Streamlit](https://docs.streamlit.io/)
- [yfinance](https://pypi.org/project/yfinance/)
- [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/)
- [TextBlob](https://pypi.org/project/textblob/)
- [pandas](https://pypi.org/project/pandas/)
- [plotly](https://pypi.org/project/plotly/)
- [sqlite3](https://www.sqlite.org/index.html)

## Como Executar Localmente

1. **Instale o Python:**
   - [Download Python](https://www.python.org/downloads/)

2. **Crie e ative um ambiente virtual:**
   ```sh
   python -m venv venv
   venv\Scripts\activate   # Windows
   source venv/bin/activate # Linux/Mac
   ```

3. **Instale as dependências:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Execute o Streamlit:**
   ```sh
   streamlit run presentations/app.py
   ```

5. **Acesse o dashboard localmente:**
   - O Streamlit irá exibir o endereço local no terminal, geralmente http://localhost:8501

## Acesse Online

Você pode acessar o projeto online em:  
**[https://market-sentiments.streamlit.app/](https://market-sentiments.streamlit.app/)**

## Observações

- O banco de dados `InvestimentoInfoPy.db` é criado automaticamente na raiz do projeto.
- As imagens e modelagem ER estão disponíveis na pasta `arquivos/model/`.
- O projeto foi desenvolvido e testado em ambiente Windows e Linux.

## Autor

Desenvolvido por [Leandro Victor Silva](https://www.linkedin.com/in/leandro-victor-silva-8a319b228/)

Repositório: [GitHub - Leandrolsc/market_sentiment](https://github.com/Leandrolsc/market_sentiment)