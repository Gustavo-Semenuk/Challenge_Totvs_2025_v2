import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns
from ms_clusterizacao_knn.view.view_kmeans import carregar_arquivo_para_dataframe


def processar_dados_clusterizacao(caminho_arquivo, n_clusters=3):
    """
    Carrega o arquivo, realiza pré-processamento e clusterização.
    Retorna o DataFrame com a coluna 'cluster' adicionada.
    """
    # Carregar o DataFrame
    df = carregar_arquivo_para_dataframe(caminho_arquivo)
    df_clean = df.copy()

    # Conversão de vírgula para ponto e para float
    df_clean['VL_TOTAL_CONTRATO'] = df_clean['VL_TOTAL_CONTRATO'].str.replace(
        ',', '.').astype(float)
    df_clean['VLR_CONTRATACOES_12M'] = df_clean['VLR_CONTRATACOES_12M'].str.replace(
        ',', '.').astype(float)

    # Encoding para variáveis categóricas
    cols_categoricas = ['DS_SEGMENTO', 'DS_SUBSEGMENTO', 'FAT_FAIXA',
                        'MARCA_TOTVS', 'MODAL_COMERC', 'SITUACAO_CONTRATO']
    le = LabelEncoder()
    for col in cols_categoricas:
        df_clean[col] = le.fit_transform(df_clean[col].astype(str))

    # Selecionar colunas para clusterização
    colunas_cluster = ['VL_TOTAL_CONTRATO', 'VLR_CONTRATACOES_12M',
                       'QTD_CONTRATACOES_12M', 'DS_SEGMENTO', 'DS_SUBSEGMENTO', 'FAT_FAIXA']
    X = df_clean[colunas_cluster]

    # Padronizar dados
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Criar clusters
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    df_clean['cluster'] = kmeans.fit_predict(X_scaled)

    return df_clean


def gerar_tabela_clientes_clusters(df):
    """
    Retorna a tabela de CD_CLIENTE com seus respectivos clusters.
    """
    tabela_clientes_clusters = df[['CD_CLIENTE', 'cluster']]
    return tabela_clientes_clusters


def plotar_grafico_clusters(df, x_col='VL_TOTAL_CONTRATO', y_col='VLR_CONTRATACOES_12M'):
    """
    Plota um gráfico de dispersão dos clusters usando duas variáveis numéricas.
    """
    plt.figure(figsize=(10, 6))
    sns.scatterplot(
        data=df,
        x=x_col,
        y=y_col,
        hue='cluster',
        palette='Set2',
        alpha=0.7
    )
    plt.title(f'Grupos de Clusters: {x_col} x {y_col}')
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.legend(title='Cluster')
    plt.tight_layout()
    plt.show()
