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
    Retorna:
      {
        "cluster_id": "1",
        "justificativa": "texto explicando a escolha"
      }
    """
    cluster_service = ClusterDataService()
    catalog_df: pd.DataFrame = cluster_service.get_catalog()

    clusters_json = catalog_df[["cluster_id", "descricao"]].to_dict(orient="records")

    prompt = f"""
    Usuário descreveu:
    "{user_input}"

    Clusters disponíveis (id e descrição):
    {json.dumps(clusters_json, ensure_ascii=False)}

    1 - Escolha o cluster mais adequado (retorne o cluster_id).
    2 - Em 2 a 3 frases, explique por que este cluster é o mais adequado.
    Responda em JSON no formato:
    {{
      "cluster_id": "<id>",
      "justificativa": "<texto>"
    }}
    """

    payload = {"model": MODEL_NAME, "prompt": prompt, "temperature": 0}
    r = requests.post(OLLAMA_URL, json=payload)
    r.raise_for_status()
    data = r.json()

    text = data.get("completion") or data["choices"][0]["text"]
    result = json.loads(text)

    return result


def obter_dados_cluster_por_nome(nome_cluster: str) -> pd.DataFrame:
    """
    Lê o parquet correspondente ao nome do cluster.
    Se não encontrar, retorna o cluster_1.
    """
    arquivo_parquet = os.path.join(PASTA_ARQUIVOS, f"{nome_cluster}.parquet")

    if not os.path.exists(arquivo_parquet):
        arquivo_parquet = os.path.join(PASTA_ARQUIVOS, "cluster_1.parquet")

    return pd.read_parquet(arquivo_parquet)


def responder_pergunta_cluster(cluster_id: str, pergunta: str) -> str:
    """
    Usuário pode fazer perguntas sobre o cluster já escolhido.
    """
    cluster_service = ClusterDataService()
    catalog_df = cluster_service.get_catalog()
    info = catalog_df[catalog_df["cluster_id"] == int(cluster_id)].iloc[0].to_dict()

    prompt = f"""
    Você é um especialista em clusters.
    Informações do cluster selecionado:
    {json.dumps(info, ensure_ascii=False)}

    Pergunta do usuário:
    "{pergunta}"

    Responda de forma objetiva e clara.
    """

    payload = {"model": MODEL_NAME, "prompt": prompt, "temperature": 0.3}
    r = requests.post(OLLAMA_URL, json=payload)
    r.raise_for_status()
    data = r.json()
    return data.get("completion") or data["choices"][0]["text"]