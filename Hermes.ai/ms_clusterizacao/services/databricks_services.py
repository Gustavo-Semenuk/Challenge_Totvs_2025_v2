import os
import pandas as pd
from databricks import sql
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

class ClusterDataService:
    def __init__(self):
        base_dir = os.path.dirname(__file__)
        self.parquet_dir = os.path.join(base_dir, "..", "arquivo_parquet")
        self.catalog_path = os.path.join(self.parquet_dir, "cluster_catalog.parquet")

    def get_catalog(self) -> pd.DataFrame:
        return pd.read_parquet(self.catalog_path)

    def get_cluster_data_por_nome(self, nome_cluster: str) -> pd.DataFrame:
        arquivo_parquet = os.path.join(self.parquet_dir, f"{nome_cluster}.parquet")
        if not os.path.exists(arquivo_parquet):
            arquivo_parquet = os.path.join(self.parquet_dir, "cluster_1.parquet")
        return pd.read_parquet(arquivo_parquet)

    def get_cluster_data(self, cluster_id: int) -> pd.DataFrame:
        # Busca pelo cluster_id no catálogo para obter o nome
        catalog = self.get_catalog()
        match = catalog[catalog["cluster_id"] == cluster_id]
        if not match.empty:
            nome_cluster = match.iloc[0]["nome"]
        else:
            nome_cluster = "cluster_1"
        return self.get_cluster_data_por_nome(nome_cluster)