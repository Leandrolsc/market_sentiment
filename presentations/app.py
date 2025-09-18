import streamlit as st
import sys
import os
from streamlit_option_menu import option_menu

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from presentations.custom_pages import metricas, tabelas

st.set_page_config(
    page_title="Inicio",
    page_icon = "🏠",
    layout= 'wide',
    initial_sidebar_state="expanded",
    menu_items={
        'Report a bug': "https://github.com/Leandrolsc/market_sentiment/issues",
        'About': """
        ## Sobre o Projeto
        market_sentiment é um projeto de análise de sentimento de mercado que utiliza dados de cotações e notícias para fornecer insights valiosos aos investidores.
        """
    }
)



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
    st.title("🏠 Introdução")
    st.markdown("---")

    st.markdown("""

    """)


st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; font-size: 0.95em;'>
        Desenvolvido por: 
        <a href='https://www.linkedin.com/in/leandro-victor-silva-8a319b228/' target='_blank'><b>Leandro Victor Silva</b></a> e 
        Repositório do projeto: 
        <a href='https://github.com/Leandrolsc/market_sentiment' target='_blank'>
           <b>GitHub - Leandrolsc/market_sentiment</b>
        </a>
    </div>
    """,
    unsafe_allow_html=True
)

