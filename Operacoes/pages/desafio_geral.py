import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import os

st.set_page_config(page_title="📊 Desempenho Geral", layout="wide")
st.title("📦 Desempenho Geral dos Colaboradores")

# Protege a página: só Líder pode ver
if "logado" not in st.session_state or not st.session_state.logado:
    st.error("❌ Faça login para acessar esta página.")
    st.stop()

if st.session_state.funcao != "Líder":
    st.warning("🔒 Apenas líderes podem visualizar esta página.")
    st.stop()

# Define caminho absoluto para o banco
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
DB_PATH = os.path.join(BASE_DIR, "usuarios.db")
conn = sqlite3.connect(DB_PATH

# Garante que a tabela existe (evita erro no deploy)
def criar_tabela_relatorios():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS relatorios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT NOT NULL,
            funcao TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

criar_tabela_relatorios()

# Conexão e leitura de dados
conn = sqlite3.connect(DB_PATH)
df = pd.read_sql_query("""
    SELECT usuario, funcao, quantidade, timestamp
    FROM relatorios
""", conn)
conn.close()

# Verifica se há dados
if df.empty:
    st.info("Nenhum dado registrado ainda.")
    st.stop()

# Processa timestamp
df["timestamp"] = pd.to_datetime(df["timestamp"])
df["Ano"] = df["timestamp"].dt.year
df["Mês"] = df["timestamp"].dt.strftime('%B')
df["Dia"] = df["timestamp"].dt.date
df["Semana"] = df["timestamp"].dt.strftime("Sem. %U")
df["Turno"] = df["timestamp"].dt.hour

# Classifica turno
def classificar_turno(hora):
    if 6 <= hora < 15:
        return "1º Turno"
    elif 15 <= hora < 23:
        return "2º Turno"
    else:
        return "3º Turno"

df["Turno"] = df["Turno"].apply(classificar_turno)

# Filtros
periodo = st.selectbox("📆 Agrupar por período:", ["Dia", "Semana", "Mês", "Ano"])
funcao_filtro = st.multiselect("🧩 Filtrar por função:", df["funcao"].unique(), default=list(df["funcao"].unique()))
df = df[df["funcao"].isin(funcao_filtro)]

# Agrupamento
df_group = df.groupby([periodo, "usuario", "Turno"])["quantidade"].sum().reset_index()

# Gráfico
st.subheader("📊 Quantidade de Paletes Carregados (por período e turno)")

fig = px.bar(
    df_group,
    x=periodo,
    y="quantidade",
    color="Turno",
    barmode="group",
    facet_col="usuario",
    labels={"quantidade": "Qtd. Paletes"},
    title="Total e Distribuição de Paletes por Turno e Colaborador"
)

fig.update_layout(xaxis_title="Período", yaxis_title="Qtd. Paletes", legend_title="Turno")
st.plotly_chart(fig, use_container_width=True)

