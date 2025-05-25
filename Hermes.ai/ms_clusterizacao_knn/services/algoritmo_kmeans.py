import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns

# Carregar o DataFrame
df = pd.read_csv('/mnt/data/export.csv')

# Pré-processamento
df_clean = df.copy()

# Conversão de vírgula para ponto em campos numéricos e transformação em float
df_clean['VL_TOTAL_CONTRATO'] = df_clean['VL_TOTAL_CONTRATO'].str.replace(',', '.').astype(float)
df_clean['VLR_CONTRATACOES_12M'] = df_clean['VLR_CONTRATACOES_12M'].str.replace(',', '.').astype(float)

# Encoding para variáveis categóricas
cols_categoricas = ['DS_SEGMENTO', 'DS_SUBSEGMENTO', 'FAT_FAIXA', 'MARCA_TOTVS', 'MODAL_COMERC', 'SITUACAO_CONTRATO']
le = LabelEncoder()
for col in cols_categoricas:
    df_clean[col] = le.fit_transform(df_clean[col].astype(str))

# Selecionar colunas para clusterização
colunas_cluster = ['VL_TOTAL_CONTRATO', 'VLR_CONTRATACOES_12M', 'QTD_CONTRATACOES_12M', 'DS_SEGMENTO', 'DS_SUBSEGMENTO', 'FAT_FAIXA']
X = df_clean[colunas_cluster]

# Padronizar dados
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Encontrar o número ideal de clusters (método do cotovelo)
inertia = []
for k in range(1, 10):
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(X_scaled)
    inertia.append(kmeans.inertia_)

plt.figure(figsize=(8, 4))
plt.plot(range(1, 10), inertia, marker='o')
plt.xlabel('Número de Clusters')
plt.ylabel('Inércia')
plt.title('Método do Cotovelo')
plt.show()

# Definir número de clusters (ex: 3)
kmeans = KMeans(n_clusters=3, random_state=42)
df_clean['cluster'] = kmeans.fit_predict(X_scaled)

# Análise Exploratória dos Clusters
print(df_clean.groupby('cluster').mean())

# Visualizar os clusters
sns.pairplot(df_clean, hue='cluster', vars=['VL_TOTAL_CONTRATO', 'VLR_CONTRATACOES_12M'])
plt.show()
