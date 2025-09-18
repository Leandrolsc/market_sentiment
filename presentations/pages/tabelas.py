import streamlit as st
from use_cases.Ticker import Ticker
from use_cases.Cotacoes import Cotacoes
from use_cases.Noticias import Noticias
from datetime import datetime
import plotly.express as px

def exibir():
    """
    Página de Tabelas
    """

    st.set_page_config(page_title="Tabelas"
                        ,page_icon = "🔽"
                        ,layout= 'wide')

    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    with st.container():
        st.subheader("🔽 Download das Tabelas")
        st.write("Download de todas as informações dos tickers que foram buscados.")
        st.write("Repositorio: [Clique aqui](https://github.com/Leandrolsc/InvestimentoInfoPy)")
        st.write("---")

    @st.cache_data
    def convert_df(df):
        return df.to_csv().encode("utf-8")

    consulta_tickers = Ticker.consulta_ticker()
    st.write('Tickers')
    st.dataframe(consulta_tickers)        
    ct = convert_df(consulta_tickers)
    file_nametickers = f"Tickers_{current_time}.csv"
    st.download_button(
        label="Download Tabela com os Tickers",
        data=ct,
        file_name=file_nametickers,
        mime="text/csv",
    )



    consulta_cotacoes = Cotacoes.consulta_cotacoes()
    st.write('Cotacoes')
    st.dataframe(consulta_cotacoes)        
    ct = convert_df(consulta_cotacoes)
    file_namecotacoes = f"Cotacoes_{current_time}.csv"
    st.download_button(
        label="Download Tabela com as Cotacoes",
        data=ct,
        file_name=file_namecotacoes,
        mime="text/csv",
    )

    st.write('Noticias')
    consulta_noticias = Noticias.consulta_noticias()
    st.dataframe(consulta_noticias)        
    ct = convert_df(consulta_noticias)
    file_namenoticias = f"Noticias_{current_time}.csv"
    st.download_button(
        label="Download Tabela com as Noticias",
        data=ct,
        file_name=file_namenoticias,
        mime="text/csv",
    )
