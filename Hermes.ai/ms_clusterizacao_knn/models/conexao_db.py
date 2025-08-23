import os
import streamlit as st
import pandas as pd
from databricks import sql
from databricks.sdk.core import Config


# Configure o Databricks (use variáveis de ambiente para segurança)
cfg = Config(
    host="dbc-d3ad9dd2-0f96.cloud.databricks.com",
    token=os.getenv("DATABRICKS_TOKEN")  # export DATABRICKS_TOKEN="seu_token"
)


@st.cache_resource  # conexão é cacheada
def get_connection(http_path: str):
    return sql.connect(
        server_hostname=cfg.host,
        http_path=http_path,
        access_token=cfg.token
    )


def read_table(table_name: str, conn):
    with conn.cursor() as cursor:
        query = f"SELECT * FROM {table_name}"
        cursor.execute(query)
        return cursor.fetchall_arrow().to_pandas()


# 🔹 Configure sua warehouse
http_path_input = "/sql/1.0/warehouses/f1a172f76bf497d7"

# 🔹 Nome da tabela
table_name = "workspace.default.validation_totvs"

if http_path_input and table_name:
    conn = get_connection(http_path_input)
    df = read_table(table_name, conn)
    df
