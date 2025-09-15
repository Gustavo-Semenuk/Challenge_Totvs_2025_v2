import json
import requests
import pandas as pd
from ms_clusterizacao.services.databricks_services import ClusterDataService

OLLAMA_URL = "http://localhost:11434/v1/completions"
MODEL_NAME = "llama3:latest"

def escolher_cluster(user_input: str) -> dict:
    cluster_service = ClusterDataService()
    catalog_df = cluster_service.get_catalog()

    clusters_json = catalog_df[["cluster_id", "descricao"]].to_dict(orient="records")

    prompt = f"""
Você é um assistente de clusterização que traduz a descrição do usuário para o cluster mais adequado.
Caso não ache nada similar, escolha o cluster_1 (cluster_id = 0), que é genérico.

Usuário descreveu:
"{user_input}"

Clusters disponíveis e suas descrições:
{json.dumps(clusters_json, ensure_ascii=False)}

Responda SOMENTE com o 'cluster_id' do cluster mais adequado.
"""
    payload = {"model": MODEL_NAME, "prompt": prompt, "temperature": 0}
    response = requests.post(OLLAMA_URL, json=payload)
    response.raise_for_status()
    data = response.json()

    text = data.get("completion") or data["choices"][0]["text"]
    cluster_id = text.strip().replace("\n", "")

    match = catalog_df[catalog_df["cluster_id"].astype(str) == cluster_id]
    if match.empty:
        match = catalog_df[catalog_df["cluster_id"] == 0] 

    return match.to_dict(orient="records")[0]


def obter_dados_cluster(cluster_id: str) -> pd.DataFrame:
    cluster_service = ClusterDataService()
    return cluster_service.get_cluster_data(cluster_id)  
