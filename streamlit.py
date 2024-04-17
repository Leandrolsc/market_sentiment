import streamlit as st
import investpy as inv
from Ticker import Ticker

st.set_page_config(page_title="InvestimentoInfoPy")


def access_list():
    lista_tickers = inv.get_stocks_list("brazil")
    return lista_tickers


with st.container():
    st.subheader("InvestimentoInfoPy")
    st.title("Dashboard do Mercado de Ações no Brasil")
    st.write("Informações da variação de cotação e analise de sentimento")
    st.write("Repositorio: [Clique aqui](https://github.com/Leandrolsc/InvestimentoInfoPy)")
    st.write("---")


option = st.selectbox(
    'Escolha um ticker?',
    access_list())

st.write(Ticker.processo_completo(Ticker,ticker_symbol = option))
st.write('Você selecionou:', option)
