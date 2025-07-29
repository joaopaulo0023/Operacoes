import os
import streamlit as st
import pandas as pd
import sqlite3

st.set_page_config(page_title="📈 Desempenho (%) por Função", layout="wide")
st.title("📊 Análise de Desempenho por Colaborador")

# Verifica login e acesso
if "logado" not in st.session_state or not st.session_state.logado:
    st.error("❌ Faça login para acessar esta página.")
    st.stop()

if st.session_state.funcao != "Líder":
    st.warning("🔒 Apenas líderes podem visualizar esta página.")
    st.stop()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "usuarios.db")

try:
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("""
        SELECT usuario, funcao, quantidade
        FROM relatorios
    """, conn)
    conn.close()
except Exception as e:
    st.error(f"Erro ao acessar banco de dados: {e}")
    st.stop()

if df.empty:
    st.info("Nenhum dado encontrado.")
    st.stop()

# Resto do código continua igual...

