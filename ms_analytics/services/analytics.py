import os
import pandas as pd
import databricks.sql as sql

# Configurações
server_hostname = "dbc-d3ad9dd2-0f96.cloud.databricks.com"
http_path = "/sql/1.0/warehouses/f1a172f76bf497d7"
# exporte seu token antes de rodar
access_token = os.getenv("DATABRICKS_TOKEN")


def read_table(table_name: str):
    with sql.connect(
        server_hostname=server_hostname,
        http_path=http_path,
        access_token=access_token
    ) as conn:
        with conn.cursor() as cursor:
            query = f"SELECT * FROM {table_name}"
            cursor.execute(query)
            return cursor.fetchall_arrow().to_pandas()


# Nome da tabela
table_name = "workspace.default.validation_totvs"

df = read_table(table_name)
validation_totvs = df
print(df)  # ou no Streamlit -> st.dataframe(df)
