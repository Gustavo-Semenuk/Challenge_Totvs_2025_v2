import pandas as pd
from ms_analytics.Controllers.controller_s3 import obter_arquivo_como_bytes
from ms_analytics.Models.conexao_db import listar_arquivos


def carregar_arquivo_para_dataframe(file_key):
    conteudo = obter_arquivo_como_bytes(file_key)
    df = pd.read_csv(pd.io.common.BytesIO(conteudo))
    return df


'bucket-ms-upload'

listar_arquivos('bucket-ms-upload')
