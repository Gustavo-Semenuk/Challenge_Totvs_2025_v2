import pandas as pd
import csv
from io import BytesIO
from ms_analytics.controller.controller_s3 import obter_arquivo_como_bytes
from ms_analytics.controller.controller_s3 import obter_arquivos_disponiveis


def detectar_delimitador(conteudo):
    sniffer = csv.Sniffer()
    sample = conteudo.decode('utf-8').splitlines()[0]
    return sniffer.sniff(sample).delimiter


def carregar_arquivo_para_dataframe(file_key):
    conteudo = obter_arquivo_como_bytes(file_key)
    sample = conteudo.decode('utf-8').splitlines()[0]
    import csv
    delimiter = csv.Sniffer().sniff(sample).delimiter
    df = pd.read_csv(BytesIO(conteudo), sep=delimiter,
                     on_bad_lines='skip', engine='python')
    return df


def listar_arquivos_disponiveis():
    arquivos = obter_arquivos_disponiveis()
    print("Arquivos disponíveis:", arquivos)
    return arquivos
