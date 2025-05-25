from ms_analytics.Models.conexao_db import listar_arquivos, baixar_arquivo

BUCKET_NAME = 'bucket-ms-upload'


def obter_arquivos_disponiveis():
    return listar_arquivos(BUCKET_NAME)


def obter_arquivo_como_bytes(file_key):
    return baixar_arquivo(BUCKET_NAME, file_key)
