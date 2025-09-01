import os
import pandas as pd
import databricks.sql as sql
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt


server_hostname = os.getenv("SERVER_HOSTNAME")
http_path = os.getenv("HTTP_PATH")
access_token = os.getenv("DATABRICKS_TOKEN")


def read_table(table_name: str) -> pd.DataFrame:
    with sql.connect(
        server_hostname=server_hostname,
        http_path=http_path,
        access_token=access_token
    ) as conn:
        with conn.cursor() as cursor:
            query = f"SELECT * FROM {table_name}"
            cursor.execute(query)
            # retorna direto um DataFrame pandas
            return cursor.fetchall_arrow().to_pandas()


# Nome da tabela
table_name = "workspace.default.cluster_variaveis"

df = read_table(table_name)

df = df.head(10000)

features = ['var_fat_faixa', 'var_segmento', 'var_subsegmento',
            'var_marca_totvs', 'var_uf', 'var_situacao_contrato']

X = df[features]

# Normalização
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# KMeans
kmeans = KMeans(n_clusters=3, random_state=42)
labels = kmeans.fit_predict(X_scaled)
df['Cluster'] = labels

# Determinação do melhor k (Cotovelo + Silhueta)
wcss = []
silhouette_scores = []
K = range(2, 11)

for k in K:
    kmeans = KMeans(n_clusters=k, random_state=42)
    labels = kmeans.fit_predict(X_scaled)
    wcss.append(kmeans.inertia_)
    silhouette_scores.append(silhouette_score(X_scaled, labels))

# VISUALIZAÇÃO
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

plt.figure(figsize=(8, 6))
plt.scatter(X_pca[:, 0], X_pca[:, 1], c=labels, cmap='viridis', alpha=0.7)
plt.xlabel("Componente Principal 1")
plt.ylabel("Componente Principal 2")
plt.title("Distribuição dos Clusters (PCA 2D)")
plt.colorbar(label='Cluster')
plt.show()
