from models.databricks_model import DatabricksModel
import os


class DatabricksController:
    def __init__(self):
        self.model = DatabricksModel(
            server_hostname="dbc-d3ad9dd2-0f96.cloud.databricks.com",
            http_path="/sql/1.0/warehouses/f1a172f76bf497d7",
            access_token=os.getenv("DATABRICKS_TOKEN")
        )

    def get_table_data(self, table_name: str):
        """Pega os dados da tabela usando o Model"""
        return self.model.read_table(table_name)
