import pandas as pd

df = pd.read_csv("D:\Faculdade\Challenge_Totvs_2025\Arquivos\cluster_1.csv")

df.to_parquet("cluster_1.parquet", engine="pyarrow", index=False)


import pandas as pd
import os

# Caminho do CSV de entrada
csv_path = r"D:\Faculdade\Challenge_Totvs_2025\Arquivos\cluster_1.csv"

# Pasta de saída para Parquet
output_folder = r"D:\Faculdade\Challenge_Totvs_2025\Hermes.ai\ms_clusterizacao\arquivo_parquet"

# Nome do arquivo Parquet
parquet_path = os.path.join(output_folder, "cluster_1.parquet")

# Lendo CSV
df = pd.read_csv(csv_path)

# Convertendo para Parquet
df.to_parquet(parquet_path, engine='pyarrow', index=False)

print(f"Arquivo Parquet salvo em: {parquet_path}")