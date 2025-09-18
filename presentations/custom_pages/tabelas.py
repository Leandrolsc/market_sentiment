import streamlit as st
import pandas as pd
from use_cases.Ticker import Ticker
from use_cases.Cotacoes import Cotacoes
from use_cases.Noticias import Noticias
from datetime import datetime

# --- Funções de Carregamento de Dados ---

@st.cache_data(ttl=600) # Cache de 10 minutos
def carregar_dados_tickers():
    """
    Carrega e armazena em cache os dados de todos os tickers.
    Retorna um DataFrame vazio em caso de erro.
    """
    try:
        return Ticker.consulta_ticker()
    except Exception as e:
        st.error(f"Erro ao carregar os dados dos Tickers: {e}")
        return pd.DataFrame()

@st.cache_data(ttl=600) # Cache de 10 minutos
def carregar_dados_cotacoes():
    """
    Carrega e armazena em cache os dados de todas as cotações.
    Retorna um DataFrame vazio em caso de erro.
    """
    try:
        return Cotacoes.consulta_cotacoes()
    except Exception as e:
        st.error(f"Erro ao carregar os dados das Cotações: {e}")
        return pd.DataFrame()

@st.cache_data(ttl=600) # Cache de 10 minutos
def carregar_dados_noticias():
    """
    Carrega e armazena em cache os dados de todas as notícias.
    Retorna um DataFrame vazio em caso de erro.
    """
    try:
        return Noticias.consulta_noticias()
    except Exception as e:
        st.error(f"Erro ao carregar os dados das Notícias: {e}")
        return pd.DataFrame()

# --- Funções de Exibição (Componentes da UI) ---

@st.cache_data
def convert_df_to_csv(df):
    """
    Converte um DataFrame para CSV, otimizado para cache.
    """
    return df.to_csv(index=False).encode("utf-8")

def exibir_tabela_para_download(titulo, df, nome_base_arquivo):
    """
    Exibe um título, um DataFrame e um botão de download para o mesmo.
    Trata casos onde o DataFrame está vazio.
    
    Args:
        titulo (str): O título a ser exibido acima da tabela.
        df (pd.DataFrame): O DataFrame a ser exibido.
        nome_base_arquivo (str): O nome base para o arquivo CSV.
    """
    st.write("---")
    st.subheader(titulo)

    if df.empty:
        st.info(f"Não há dados disponíveis para '{titulo}'.")
        return

    st.dataframe(df)
    
    csv_data = convert_df_to_csv(df)
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M")
    file_name = f"{nome_base_arquivo}_{current_time}.csv"
    
    st.download_button(
        label=f"Download da Tabela '{titulo}'",
        data=csv_data,
        file_name=file_name,
        mime="text/csv",
    )

# --- Função Principal da Página ---

def exibir():
    """
    Página de Tabelas
    """
    st.title("Tabelas para Download")
    st.write("Faça o download de todas as informações que foram buscadas e armazenadas pela aplicação.")
    st.write("Repositório: [Clique aqui](https://github.com/Leandrolsc/InvestimentoInfoPy)")

    with st.spinner("Carregando dados das tabelas..."):
        # Carrega todos os dados primeiro
        df_tickers = carregar_dados_tickers()
        df_cotacoes = carregar_dados_cotacoes()
        df_noticias = carregar_dados_noticias()

    # Exibe cada tabela e seu botão de download
    exibir_tabela_para_download("Tickers", df_tickers, "Tickers")
    exibir_tabela_para_download("Cotações", df_cotacoes, "Cotacoes")
    exibir_tabela_para_download("Notícias", df_noticias, "Noticias")

# Se quiser rodar este arquivo diretamente
if __name__ == "__main__":
    exibir()
