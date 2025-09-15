import os
import pandas as pd
from databricks import sql
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()


class DatabricksService:
    def __init__(self):
        server = os.getenv("SERVER_HOSTNAME")
        path = os.getenv("HTTP_PATH")
        token = os.getenv("DATABRICKS_TOKEN")

        if not all([server, path, token]):
            raise ValueError(
                "As variáveis SERVER_HOSTNAME, HTTP_PATH e DATABRICKS_TOKEN devem estar definidas!")

        self.conn = sql.connect(
            server_hostname=server,
            http_path=path,
            access_token=token
        )

    def read_table(self, table_name: str) -> pd.DataFrame:
        with self.conn.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {table_name}")
            result = cursor.fetchall()
            cols = [desc[0] for desc in cursor.description]
            return pd.DataFrame(result, columns=cols)

    def close(self):
        self.conn.close()


class ClusterDataService:
    def __init__(self):
        base_dir = os.path.dirname(__file__)  # caminho da pasta atual (services)
        # se o arquivo está em Hermes.ai/ms_clusterizacao/cluster_catalog.parquet
        self.catalog_path = os.path.join(base_dir, "..","arquivo_parquet" ,"cluster_catalog.parquet")

    def get_catalog(self) -> pd.DataFrame:
        return pd.read_parquet(self.catalog_path)
