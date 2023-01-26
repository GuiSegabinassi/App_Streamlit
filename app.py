import streamlit as st
import pandas as pd
import yfinance
import plotly
from prophet import Prophet
from prophet.plot import plot_plotly, plot_components_plotly
from plotly import graph_objs as go
from datetime import datetime, timezone, date


DATA_INICIO = "2017-01-01"
DATA_FINAL = date.today()

st.title("Segabinassi Análises")

#sidebar
st.sidebar.header("Escolha uma ação")


def pegar_dados_acoes():
    path = 'acoes.csv'
    return pd.read_csv(path, delimiter = ";")

df = pegar_dados_acoes()

acao = df["snome"]  
nome_acao_escolhida = st.sidebar.selectbox("Escolha uma ação:", acao)

df_acao = df[df["snome"] == nome_acao_escolhida]
acao_escolhida = df_acao.iloc[0]["sigla_acao"]
acao_escolhida = acao_escolhida + ".SA"

@st.cache
def pegar_valores_online(sigla_acao):
    df = yfinance.download(sigla_acao, DATA_INICIO, DATA_FINAL)
    df.reset_index(inplace=True)
    return df

df_valores = pegar_valores_online(acao_escolhida)

st.subheader("Tabela de valores - " + nome_acao_escolhida)
st.write(df_valores.tail(10))


#Criando graficos
st.subheader("Gráfico de preços")
fig = go.Figure()
fig.add_trace(go.Scatter(x=df_valores["Date"],
y=df_valores["Close"],
name="Preço fechamento",
line_color="red"))

fig.add_trace(go.Scatter(x=df_valores["Date"],
y=df_valores["Open"],
name="Preço abertura",
line_color="blue"))

st.plotly_chart(fig)







