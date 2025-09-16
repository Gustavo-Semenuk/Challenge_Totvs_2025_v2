import os
import json
import pandas as pd
import requests
from ms_clusterizacao.services.databricks_services import ClusterDataService

# Caminhos relativos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # pasta services
PASTA_ARQUIVOS = os.path.join(BASE_DIR, "..", "arquivo_parquet")
CATALOG_PATH = os.path.join(PASTA_ARQUIVOS, "cluster_catalog.parquet")

OLLAMA_URL = "http://54.233.85.14:11434/v1/completions"
MODEL_NAME = "llama3:latest"


def escolher_cluster(user_input: str) -> str:
    """
    Usa LLM para decidir qual nome de cluster corresponde à descrição do usuário.
    Retorna o valor da coluna 'nome' do cluster escolhido.
    """
    # Lê catálogo
    catalog_df = pd.read_parquet(CATALOG_PATH)

    clusters_json = catalog_df[["cluster_id", "nome", "descricao", "conceito"]].to_dict(orient="records")

    prompt = f"""
Você é um assistente de clusterização que traduz a descrição do usuário para o cluster mais adequado.
Caso não ache nada similar, escolha o cluster_1 (nome = 'cluster_1').

Usuário descreveu:
"{user_input}"

Clusters disponíveis e suas descrições:
{json.dumps(clusters_json, ensure_ascii=False)}

Responda SOMENTE com o 'nome' do cluster mais adequado e o porque escolheu ele.
"""

    payload = {"model": MODEL_NAME, "prompt": prompt, "temperature": 0}
    response = requests.post(OLLAMA_URL, json=payload)
    response.raise_for_status()
    data = response.json()

    # Extrai resposta do LLM
    text = data.get("completion") or data["choices"][0]["text"]
    nome_cluster = text.strip().replace("\n", "")

    # Verifica se o nome existe no catálogo, senão usa cluster_1
    if nome_cluster not in catalog_df["nome"].values:
        nome_cluster = "cluster_1"

    return nome_cluster


def obter_dados_cluster_por_nome(nome_cluster: str) -> pd.DataFrame:
    """
    Lê o parquet correspondente ao nome do cluster.
    Se não encontrar, retorna o cluster_1.
    """
    arquivo_parquet = os.path.join(PASTA_ARQUIVOS, f"{nome_cluster}.parquet")

    if not os.path.exists(arquivo_parquet):
        arquivo_parquet = os.path.join(PASTA_ARQUIVOS, "cluster_1.parquet")

    return pd.read_parquet(arquivo_parquet)
