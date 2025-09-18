import streamlit as st
import investpy as inv
import pandas as pd
from use_cases.Ticker import Ticker
from use_cases.Cotacoes import Cotacoes
from use_cases.Noticias import Noticias
import datetime
import plotly.express as px

# --- Funções Auxiliares e de Boas Práticas ---

def get_safe(df, column, default="N/A"):
    """
    Acessa um valor em um DataFrame de forma segura.
    Retorna um valor padrão se o DataFrame estiver vazio, a coluna não existir,
    ou o valor for nulo.
    """
    if df is not None and not df.empty and column in df.columns:
        value = df[column].iloc[0]
        return value if pd.notna(value) else default
    return default

@st.cache_data(ttl=3600) # Cache por 1 hora
def carregar_lista_tickers():
    """
    Carrega e armazena em cache a lista de tickers do Brasil.
    """
    try:
        lista_tickers = inv.get_stocks_list("brazil")
        return lista_tickers
    except Exception as e:
        st.error(f"Erro ao carregar a lista de tickers: {e}")
        return []

@st.cache_data(ttl=600) # Cache por 10 minutos
def carregar_dados_ticker(ticker, data_inicio, data_fim):
    """
    Carrega todos os dados necessários para um ticker específico.
    Centraliza as chamadas de API e o tratamento de erros.
    """
    if not ticker:
        return None, None, None, None

    try:
        info_ticker = Ticker.processo_completo(Ticker, ticker_symbol=ticker)
    except Exception:
        info_ticker = pd.DataFrame() # Retorna DF vazio em caso de erro

    try:
        dados_cotacao = Cotacoes.processo_completo(Cotacoes, ticker_symbol=ticker, inicio=data_inicio, fim=data_fim)
    except Exception:
        dados_cotacao = pd.DataFrame() # Retorna DF vazio em caso de erro

    try:
        sentimento = Noticias.processo_completo(ticker)
    except Exception:
        sentimento = pd.DataFrame() # Retorna DF vazio em caso de erro
    
    try:
        top_news = Noticias.consulta_noticias_negativas(ticker)
    except Exception:
        top_news = pd.DataFrame() # Retorna DF vazio em caso de erro

    return info_ticker, dados_cotacao, sentimento, top_news

# --- Funções de Exibição (Componentes da UI) ---

def exibir_info_empresa(info_ticker):
    """Exibe o cabeçalho com informações da empresa."""
    st.write("---")
    
    # Usando a função get_safe para evitar erros
    nome = get_safe(info_ticker, 'LongName', 'Nome não disponível')
    setor = get_safe(info_ticker, 'Sector', 'Setor não disponível')
    industria = get_safe(info_ticker, 'Industry', 'Indústria não disponível')
    recomendacao = get_safe(info_ticker, 'RecomendationMean', 'N/A')

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Empresa", nome)
    col2.metric("Setor", setor)
    col3.metric("Indústria", industria)
    col4.metric("Recomendação Yahoo", f"{recomendacao}")

def exibir_metricas_financeiras(info_ticker, dados_cotacao, sentimento):
    """Exibe as métricas financeiras em colunas."""
    st.write("---")
    col1, col2, col3, col4, col5 = st.columns(5)

    # Métrica 1: Valor Atual
    preco_atual = get_safe(info_ticker, 'currentPrice', 0.0)
    preco_max_hist = dados_cotacao['Close'].max() if not dados_cotacao.empty else 0
    variacao_delta = 0
    if preco_atual > 0 and preco_max_hist > 0:
        variacao_delta = ((preco_atual / preco_max_hist) * 100) - 100
    
    col1.metric(
        "Valor Atual",
        value=f"R${preco_atual:.2f}",
        delta=f"{variacao_delta:.2f}%",
        help='Variação em relação ao valor máximo no período selecionado.'
    )

    # Métrica 2: Variação Histórica
    variacao_hist = 0
    if not dados_cotacao.empty and dados_cotacao['Close'].min() > 0:
        variacao_hist = (dados_cotacao['Close'].max() / dados_cotacao['Close'].min()) * 100
    
    col2.metric(
        "Variação no Período",
        f"{variacao_hist:.2f}%",
        help="Variação total no período selecionado (Valor Máximo / Valor Mínimo)."
    )

    # Métrica 3: Último Dividendo
    ultimo_dividendo = get_safe(info_ticker, 'lastDividendValue', 0.0)
    col3.metric(
        "Último Dividendo",
        f"R${ultimo_dividendo:.2f}",
        help="Valor do último dividendo distribuído."
    )

    # Métrica 4: Liquidez Média
    liquidez = dados_cotacao["Volume"].mean() if not dados_cotacao.empty else 0
    col4.metric(
        "Liquidez Média Diária",
        f"{liquidez:,.0f}".replace(",", "."),
        help="Volume médio de negociações diárias no período."
    )

    # Métrica 5: Sentimento Médio
    sentimento_medio = sentimento['Sentimento'].mean() if not sentimento.empty else 0
    col5.metric(
        "Sentimento Médio",
        f"{sentimento_medio:.2f}",
        help="Média de sentimento das últimas notícias (valores > 0 são positivos)."
    )

def exibir_grafico_cotacoes(ticker, info_ticker, dados_cotacao):
    """Exibe o gráfico de cotações."""
    if dados_cotacao.empty:
        st.warning("Não há dados de cotação para exibir no período selecionado.")
        return

    link = get_safe(info_ticker, 'WebSite', '#')
    nome_empresa = get_safe(info_ticker, 'LongName', ticker)
    
    fig = px.line(
        dados_cotacao,
        x='Date',
        y="Close",
        title=f"<b><a href='{link}' target='_blank'>Cotação de {ticker} - {nome_empresa}</a></b>"
    ).update_layout(
        xaxis_title="Data",
        yaxis_title="Preço de Fechamento (R$)",
        title_x=0.5
    )
    st.plotly_chart(fig, use_container_width=True)

def exibir_noticias(top_news):
    """Exibe as principais notícias em colunas."""
    st.write("---")
    st.subheader("Principais Notícias")
    
    if top_news.empty:
        st.info("Nenhuma notícia encontrada para este ativo.")
        return

    # Limita a 3 colunas, mesmo que haja mais notícias
    cols = st.columns(min(len(top_news), 3))
    
    # Itera de forma segura sobre as notícias disponíveis
    for i, row in top_news.head(len(cols)).iterrows():
        with cols[i]:
            # Supondo que a notícia esteja na primeira coluna do DataFrame
            noticia_texto = str(row.iloc[0])
            st.info(f':newspaper: {noticia_texto}')

# --- Função Principal da Página ---

def exibir():
    """
    Página de Métricas
    """
    st.title(":chart_with_upwards_trend: Dashboard do Mercado de Ações no Brasil")
    st.write("Informações sobre ações, cotações e análise de sentimento.")
    st.write("Repositório: [Clique aqui](https://github.com/Leandrolsc/market_sentiment)")
    st.write("---")

    lista_tickers = carregar_lista_tickers()
    if not lista_tickers:
        st.stop() # Interrompe a execução se não conseguir carregar os tickers

    # --- INPUTS DO USUÁRIO ---
    col1, col2, col3 = st.columns(3)
    with col1:
        ticker_selecionado = st.selectbox('Escolha um ticker:', lista_tickers)
    
    # Define as datas padrão
    data_final_padrao = datetime.date.today()
    data_inicio_padrao = datetime.date(2023, 1, 1)

    with col2:
        data_inicio = st.date_input("Selecione a data de início:", data_inicio_padrao)
    with col3:
        data_final = st.date_input("Selecione a data final:", data_final_padrao)

    # --- LÓGICA DE EXIBIÇÃO ---
    if ticker_selecionado:
        # Usando um spinner para dar feedback ao usuário durante o carregamento
        with st.spinner(f"Buscando dados para {ticker_selecionado}..."):
            info_ticker, dados_cotacao, sentimento, top_news = carregar_dados_ticker(
                ticker_selecionado, data_inicio, data_final
            )

        # Verifica se os dados essenciais foram carregados
        if info_ticker is None or info_ticker.empty:
            st.error(f"Não foi possível encontrar informações para o ticker '{ticker_selecionado}'. Verifique se o código está correto ou tente novamente.")
        else:
            exibir_info_empresa(info_ticker)
            exibir_metricas_financeiras(info_ticker, dados_cotacao, sentimento)
            exibir_grafico_cotacoes(ticker_selecionado, info_ticker, dados_cotacao)
            exibir_noticias(top_news)

# Se quiser rodar este arquivo diretamente
if __name__ == "__main__":
    exibir()
