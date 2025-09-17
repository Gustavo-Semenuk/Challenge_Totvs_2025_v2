import os
import json
import pandas as pd
import requests
from ms_clusterizacao.services.databricks_services import ClusterDataService
from dotenv import load_dotenv

load_dotenv()

# Caminhos relativos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # pasta services
PASTA_ARQUIVOS = os.path.join(BASE_DIR, "..", "arquivo_parquet")
CATALOG_PATH = os.path.join(PASTA_ARQUIVOS, "cluster_catalog.parquet")

OLLAMA_URL = "http://54.233.100.228:11434/v1/completions"
MODEL_NAME = "llama3:latest"


def escolher_cluster(user_input: str) -> dict:
    """
    Recebe a descrição do usuário, retorna:
    {
        "nome": nome do cluster escolhido,
        "justificativa": motivo da escolha
    }
    """
    # Carrega catálogo local
    catalog_df = pd.read_parquet(CATALOG_PATH)
    clusters_json = catalog_df[["nome", "descricao", "conceito"]].to_dict(orient="records")

    # Prompt para o LLM
    prompt = f"""
Você é um assistente de clusterização que traduz a descrição do usuário para o cluster mais adequado.
Caso não ache nada similar, escolha 'cluster_1'.

Usuário descreveu:
"{user_input}"

Clusters disponíveis e suas descrições:
{json.dumps(clusters_json, ensure_ascii=False)}

Responda com o NOME do cluster mais adequado e explique em uma frase porque escolheu ele.
Formato de resposta:
<nome_cluster>::<justificativa>
"""

    payload = {"model": MODEL_NAME, "prompt": prompt, "temperature": 0}
    response = requests.post(OLLAMA_URL, json=payload)
    response.raise_for_status()
    data = response.json()

    # Extrai resposta do LLM
    text = data.get("completion") or data["choices"][0]["text"]
    text = text.strip().replace("\n", "")

    # Separa nome do cluster e justificativa
    if "::" in text:
        nome_cluster, justificativa = text.split("::", 1)
    else:
        nome_cluster, justificativa = text, "Sem justificativa fornecida."

    # Verifica se o nome existe no catálogo
    if nome_cluster not in catalog_df["nome"].values:
        nome_cluster = "cluster_1"
        justificativa = "Cluster genérico utilizado pois não houve correspondência."

    return {"nome": nome_cluster, "justificativa": justificativa}


def obter_dados_cluster(nome_cluster: str) -> pd.DataFrame:
    """
    Retorna o DataFrame do cluster escolhido (usando cache local).
    """
    cluster_service = ClusterDataService()
    df = cluster_service.get_cluster_data(nome_cluster)
    return df