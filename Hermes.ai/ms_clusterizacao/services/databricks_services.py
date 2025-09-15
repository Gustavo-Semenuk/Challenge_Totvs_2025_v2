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
            raise ValueError("As variáveis SERVER_HOSTNAME, HTTP_PATH e DATABRICKS_TOKEN devem estar definidas!")

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
        # pasta onde você salva os parquet, por exemplo:
        self.base_path = Path("ms_clusterizacao/arquivo_parquet")

    def get_catalog(self) -> pd.DataFrame:
        """
        Lê o arquivo parquet local com o catálogo de clusters
        """
        catalog_path = self.base_path / "cluster_catalog.parquet"
        return pd.read_parquet(catalog_path)

    def get_cluster_data(self, cluster_id: str) -> pd.DataFrame:
        """
        Lê os dados de um cluster específico do parquet local
        """
        cluster_file = self.base_path / f"cluster_{cluster_id}.parquet"
        return pd.read_parquet(cluster_file)