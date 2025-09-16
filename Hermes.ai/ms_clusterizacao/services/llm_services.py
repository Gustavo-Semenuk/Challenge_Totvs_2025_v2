import json
import os
import pandas as pd
import requests

# Configurações
OLLAMA_URL = "http://54.233.85.14:11434/v1/completions"
MODEL_NAME = "llama3:latest"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PASTA_ARQUIVOS = os.path.join(BASE_DIR, "..", "arquivo_parquet")

CATALOG_PATH = 'cluster_catalog.parquet'

# Função para obter dados do cluster pelo nome


def obter_dados_cluster_por_nome(nome_cluster: str) -> pd.DataFrame:
    arquivos = [f for f in os.listdir(
        PASTA_ARQUIVOS) if f.endswith(".parquet")]

    for arquivo in arquivos:
        path = os.path.join(PASTA_ARQUIVOS, arquivo)
        df = pd.read_parquet(path)
        if "nome" in df.columns and nome_cluster in df["nome"].values:
            return df

    # Fallback para cluster_1
    fallback_path = os.path.join(PASTA_ARQUIVOS, "cluster_1.parquet")
    return pd.read_parquet(fallback_path)


# Função para escolher o cluster
def escolher_cluster(user_input: str) -> str:
    catalog_df = pd.read_parquet(CATALOG_PATH)
    clusters_json = catalog_df[["cluster_id", "nome",
                                "descricao", "conceito"]].to_dict(orient="records")

    prompt = f"""
Você é um assistente de clusterização que traduz a descrição do usuário para o cluster mais adequado.
Caso não ache nada similar, escolha o cluster genérico com nome 'cluster_1'.

Usuário descreveu:
"{user_input}"

Clusters disponíveis e suas descrições:
{json.dumps(clusters_json, ensure_ascii=False)}

Responda SOMENTE com o 'nome' do cluster mais adequado.
"""
    payload = {"model": MODEL_NAME, "prompt": prompt, "temperature": 0}
    response = requests.post(OLLAMA_URL, json=payload)
    response.raise_for_status()
    data = response.json()

    # Pega o nome do cluster retornado pelo LLM
    nome_cluster = data.get("completion") or data["choices"][0]["text"]
    return nome_cluster.strip()
