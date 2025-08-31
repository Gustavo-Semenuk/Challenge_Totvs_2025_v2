import pandas as pd
from services.databricks_services import ClusterDataService


cluster_service = ClusterDataService()
df = cluster_service.get_data()  # carrega do parquet ou Databricks se não existir
print(df.head())

