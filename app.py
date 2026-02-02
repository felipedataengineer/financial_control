from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from datetime import datetime
from decimal import Decimal
import os
import streamlit as st
import pandas as pd

load_dotenv()

DB_USERNAME = os.getenv('BD_USER')
encoded_password = os.getenv('BD_PASSWORD')
DB_HOST = os.getenv('BD_HOST')
DB_PORT = os.getenv('BD_PORT')
DB_NAME = os.getenv('BD_NAME')


engine = create_engine(f'postgresql+psycopg2://{DB_USERNAME}:{encoded_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}', pool_pre_ping=True,pool_recycle=300)



# def teste_unidade_db():
#     engine_test = create_engine(f'postgresql+psycopg2://{DB_USERNAME}:{encoded_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}', 
#                         pool_pre_ping=True, pool_recycle=300, connect_args={'connect_timeout': 2})

#     try:
#         with engine_test.connect() as conn:
#             conn.execute(text("SELECT 1"))
#             print('ok')
#     except:
#         print('deu ruim')

# # teste_unidade_db()






def inserir_dado(tabela, data,descricao,valor,categoria,conta):
    sql = text(f"""
        INSERT INTO {tabela} (data,descricao,valor,categoria,conta)
        VALUES (:data, :descricao, :valor, :categoria, :conta)
    """)

    with engine.begin() as conn:
        conn.execute(sql, {"data": data, "descricao": descricao, "valor": valor, "categoria": categoria, "conta": conta})



#calcular saldo
def saldo(tabela):
    # Validação do nome da tabela (importante!)
    tabelas_validas = ['despesas', 'receitas', 'investimentos']
    if tabela not in tabelas_validas:
        raise ValueError(f"Tabela {tabela} inválida")
    
    sql = text(f"SELECT COALESCE(SUM(valor), 0) AS saldo FROM {tabela}")
    with engine.connect() as conn:
        result = conn.execute(sql)
        return result.scalar()  # Método melhor que fetchone()





st.title("Controle Financeiro")


st.metric("Saldo Atual", saldo('despesas'))


with st.sidebar:
    st.header('tabela')


def teste():
    print('teste')
st.button('botaoteste', key=None, help=None, on_click=teste())