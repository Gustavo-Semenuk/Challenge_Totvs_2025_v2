import os
import databricks.sql as sql
import pandas as pd


class DatabricksModel:
    def __init__(self, server_hostname: str, http_path: str, access_token: str):
        self.server_hostname = server_hostname
        self.http_path = http_path
        self.access_token = access_token

    def read_table(self, table_name: str) -> pd.DataFrame:
        """Lê a tabela do Databricks e retorna um DataFrame"""
        with sql.connect(
            server_hostname=self.server_hostname,
            http_path=self.http_path,
            access_token=self.access_token
        ) as conn:
            with conn.cursor() as cursor:
                query = f"SELECT * FROM {table_name}"
                cursor.execute(query)
                return cursor.fetchall_arrow().to_pandas()
