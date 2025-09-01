import pandas as pd
import matplotlib.pyplot as plt
import os
from ms_clusterizacao.services.databricks_services import ClusterDataService
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA


cluster_service = ClusterDataService()
df = cluster_service.get_data().head(10000)  # carrega do parquet ou Databricks se não existir

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
K = range(3, 5)

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