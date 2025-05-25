import pandas as pd
import csv
from io import BytesIO
from ms_analytics.controller.controller_s3 import obter_arquivo_como_bytes
from ms_analytics.controller.controller_s3 import obter_arquivos_disponiveis


def detectar_delimitador(conteudo):
    sniffer = csv.Sniffer()
    sample = conteudo.decode('utf-8').splitlines()[0]
    return sniffer.sniff(sample).delimiter


# def carregar_arquivo_para_dataframe(file_key):
 #   conteudo = obter_arquivo_como_bytes(file_key)
 #   delimiter_detectado = detectar_delimitador(conteudo)
 #   df = pd.read_csv(pd.io.common.BytesIO(conteudo), sep=";",encoding='latin1')
 #   return df

def carregar_arquivo_para_dataframe(file_key):
    buffer = BytesIO(file_key)  # cria um buffer de memória a partir dos bytes
    # usa o delimitador ";"
    df = pd.read_csv(buffer, delimiter=';', encoding='utf-8')
    return df


def listar_arquivos_disponiveis():
    arquivos = obter_arquivos_disponiveis()
    print("Arquivos disponíveis:", arquivos)
    return arquivos
