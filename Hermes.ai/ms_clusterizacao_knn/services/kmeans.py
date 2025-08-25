import os
import pandas as pd
import databricks.sql as sql
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt


def rodar_kmeans(table_name="workspace.default.cluster_variaveis", n_clusters=3):
    # Conexão Databricks
    server_hostname = "dbc-d3ad9dd2-0f96.cloud.databricks.com"
    http_path = "/sql/1.0/warehouses/f1a172f76bf497d7"
    access_token = os.getenv("DATABRICKS_TOKEN")

    # Função para ler a tabela
    def read_table(table_name: str) -> pd.DataFrame:
        with sql.connect(
            server_hostname=server_hostname,
            http_path=http_path,
            access_token=access_token
        ) as conn:
            with conn.cursor() as cursor:
                query = f"SELECT * FROM {table_name}"
                cursor.execute(query)
                return cursor.fetchall_arrow().to_pandas()

    # Leitura dos dados
    df = read_table(table_name)

    # Seleção das features numéricas
    features = ['var_fat_faixa', 'var_segmento', 'var_subsegmento',
                'var_marca_totvs', 'var_uf', 'var_situacao_contrato']

    X = df[features]

    # Normalização
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Rodar KMeans
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    labels = kmeans.fit_predict(X_scaled)
    df['Cluster'] = labels

    # PCA para visualização 2D
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_scaled)

    return df, X_pca, labels
