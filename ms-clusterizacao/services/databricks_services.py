import os
import pandas as pd
import databricks.sql as sql
from dotenv import load_dotenv

load_dotenv()


class DatabricksService:
    def __init__(self):
        server = os.getenv("SERVER_HOSTNAME")
        path = os.getenv("HTTP_PATH")
        token = os.getenv("DATABRICKS_TOKEN")

        if not all([server, path, token]):
            raise ValueError(
                "As variáveis de ambiente SERVER_HOSTNAME, HTTP_PATH e DATABRICKS_TOKEN devem estar definidas!"
            )

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
    def __init__(self, data_path="cluster_variaveis.parquet"):
        self.data_path = data_path
        self.df = None
        self.db_service = DatabricksService()  # instância do serviço Databricks

    def load_data(self):
        """Carrega os dados do arquivo parquet ou do Databricks se não existir."""
        if self.df is not None:
            return self.df  # já carregado na memória

        try:
            self.df = pd.read_parquet(self.data_path)
            print(f"Dados carregados do arquivo {self.data_path}")
        except FileNotFoundError:
            print("Arquivo parquet não encontrado. Buscando do Databricks...")
            self.df = self.db_service.read_table(
                "workspace.default.cluster_variaveis")
            self.df.to_parquet(self.data_path, index=False)
            print(f"Dados salvos em {self.data_path} para uso futuro")

        return self.df

    def get_data(self) -> pd.DataFrame:
        """Retorna os dados carregados na memória (load_data deve ser chamado primeiro)"""
        if self.df is None:
            return self.load_data()
        return self.df
