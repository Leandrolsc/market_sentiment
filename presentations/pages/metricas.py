import streamlit as st
import investpy as inv
from use_cases.Ticker import Ticker
from use_cases.Cotacoes import Cotacoes
from use_cases.Noticias import Noticias
import datetime
import plotly.express as px


def exibir():
    """
    Página de Métricas
    """

    st.set_page_config(page_title="Metricas"
                    ,page_icon = "📈"
                    ,layout= 'wide')

    @st.cache_data

    def access_list():
        lista_tickers = inv.get_stocks_list("brazil")
        return lista_tickers


    with st.container():
        st.subheader("InvestimentoInfoPy")
        st.title(":chart_with_upwards_trend: Dashboard do Mercado de Ações no Brasil")
        st.write("Informações sobre ações e analise de sentimento")
        st.write("Repositorio: [Clique aqui](https://github.com/Leandrolsc/InvestimentoInfoPy)")
        st.write("---")




    today = datetime.datetime.now()
    data_inicio = datetime.date(2023,1, 1)



    coluna1, coluna2, coluna3 = st.columns(3)

    with coluna1:
        option = st.selectbox(
        'Escolha um ticker?',
        access_list())


    with coluna2:
        data_inicio = st.date_input(
                        "Selecione data de inicio:",data_inicio
                            )
    with coluna3:
        data_final = st.date_input(
                        "Selecione data final:",today
                            )


    ticker_table = Ticker.processo_completo(Ticker,ticker_symbol = option)
    dados_cotacao = Cotacoes.processo_completo(Cotacoes,ticker_symbol = option,inicio = data_inicio, fim = data_final)


    name_1, sector_2, industry_3,recomendation_mean_4  = st.columns(4)
    with name_1:
        name = ticker_table['LongName'].iloc[0]
        name_1 = st.write(f'Empresa: {name}')
    with sector_2:
        sector = ticker_table['Sector'].iloc[0]
        sector_2 = st.write(f'Sector: {sector}')
    with industry_3:
        industry = ticker_table['Industry'].iloc[0]
        industry_3 = st.write(f'Industry: {industry}')
    with recomendation_mean_4:
        recomendation_mean = ticker_table['RecomendationMean'].iloc[0]
        recomendation_mean_4 = st.write(f'Recomendacao Yahoo: {recomendation_mean}')



    sentimento = Noticias.processo_completo(option)
    max_hist,value_hist,dividend, liquidez_media, sentiment_mean = st.columns(5)

    variacao = round(((ticker_table['currentPrice']/dados_cotacao['Close'].max())*100)-100,2)
    currentPrice = ticker_table['currentPrice']
    max_hist.metric("Valor Atual"
                    ,value = f"R${float(ticker_table['currentPrice'].iloc[0])}"
                    ,delta = f"{float(variacao.iloc[0])}%" 
                    ,help='Valor Atual x variação((Valor Atual / Valor Maximo * 100) - 100))'
                    )

    value_hist.metric("Variação"
                    ,f"{round((dados_cotacao['Close'].max()/dados_cotacao['Close'].min())*100,2)}%"
                    ,help = "Quanto a ação já valorizou (Valor Maximo / Valor Minimo * 100 = Variação total)" 
                    )

    last_dividend = round(ticker_table['lastDividendValue'].iloc[0],2)
    dividend.metric("Ultimo Dividendo"
                    ,f"R${last_dividend}"
                    ,help = "Valor do ultimo dividendo distribuido")

    liquidez = round(dados_cotacao["Volume"].mean(),2)
    liquidez_media.metric("Liquidez Media"
                        ,f"{liquidez}"
                        ,help = "Liquidez media diaria de acordo com o volume movimentado"
                            )
    sentiment = round(sentimento['Sentimento'].mean(),2)
    sentiment_mean.metric ("Sentimento Medio"
                            ,f"{sentiment}"
                            ,help= "Media de sentimento das ultimas noticias")



    link = f"{ticker_table['WebSite'].iloc[0]}"
    company = str(ticker_table['LongName'].iloc[0])
    print(company)
    grafico1 = px.line(dados_cotacao
                    ,x='Date'
                    ,y="Close"
                    ).update_layout(
        xaxis_title="Date"
        ,yaxis_title = "Cotacao"
        ,title={
            'text': f"<b><a href='{link}'> {option} - {company} </a></b>",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
            })
    st.plotly_chart(grafico1,use_container_width = True)


    top_news = Noticias.consulta_noticias_negativas(option)

    col1_new, col2_new, col3_new = st.columns(3)

    cont1_new = col1_new.container(height=150)
    cont1 = str(top_news.iloc[0].values)
    cont1_new.write(':newspaper: ' + cont1.replace('[','').replace(']','').replace("'",''))

    cont2_new = col2_new.container(height=150)
    cont2 = str(top_news.iloc[1].values)
    cont2_new.write(':newspaper:  ' + cont2.replace('[','').replace(']','').replace("'",''))

    cont3_new = col3_new.container(height=150)
    cont3 = str(top_news.iloc[2].values)
    cont3_new.write(':newspaper:  ' + cont3.replace('[','').replace(']','').replace("'",''))



