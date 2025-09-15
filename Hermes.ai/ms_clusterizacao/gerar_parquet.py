import pandas as pd

df = pd.read_csv("D:\Faculdade\Challenge_Totvs_2025\Arquivos\cluster_1.csv")

df.to_parquet("cluster_1.parquet", engine="pyarrow", index=False)