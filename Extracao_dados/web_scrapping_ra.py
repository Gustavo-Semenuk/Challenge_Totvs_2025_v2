# Importa as bibliotecas necessárias
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import datetime
import pandas as pd
import numpy as np
import openpyxl

# Define o caminho para o chromedriver
chromedriver = "C:/Users/Gustavo/ChromeDriver/chromedriver.exe"

# Configurações do Chrome
options = Options()
options.add_argument("--start-maximized")

# Instancia o navegador com Service
service = Service(chromedriver)
navegador = webdriver.Chrome(service=service, options=options)

# Seleciona a página desejada
navegador.get("https://www.reclameaqui.com.br/empresa/{}/".format('totvs'))

# Cria um intervalo de espera de 2 segundos
time.sleep(2)

# Localiza o botão para aceitar cookies e clica (se existir)
try:
    navegador.find_element("xpath", '/html/body/div[2]/div[2]/a[1]').click()
except:
    print("Botão de cookies não encontrado.")

# Rola a página 300 pixels para baixo
navegador.execute_script("window.scrollBy(0, 300)")

# Define os períodos de dados desejados e seus caminhos html
periodos = {
    'seis_meses': '//*[@id="reputation-tab-1"]',
    'doze_meses': '//*[@id="reputation-tab-2"]',
    'geral': '//*[@id="reputation-tab-5"]'
}

# Define os elementos a serem coletados e seus caminhos html
elementos = {
    'nota_geral': '//*[@id="reputation"]/div[1]/div[1]/div[2]/span[2]/b',
    'num_reclamacoes': '//*[@id="reputation"]/div[1]/div[2]/a[1]/div/div/b',
    'num_respondidas': '//*[@id="reputation"]/div[1]/div[2]/a[2]/div/div/b',
    'perc_recl_resp': '//*[@id="reputation"]/div[2]/div[1]/div[1]/span',
    'novam_negoc': '//*[@id="reputation"]/div[2]/div[1]/div[2]/span',
    'indice_solucao': '//*[@id="reputation"]/div[2]/div[1]/div[3]/span',
    'nota_consumidor': '//*[@id="reputation"]/div[2]/div[1]/div[4]/span'
}

# Cria listas que conterão os dados de cada indicador
listas = {key: [] for key in elementos.keys()}

# Define o momento da coleta dos dados
agora = datetime.datetime.now()

# Percorre os períodos definidos
for periodo in periodos:
    time.sleep(1)
    navegador.find_element("xpath", periodos[periodo]).click()
    time.sleep(1)

    for elemento in elementos:
        element = navegador.find_element("xpath", elementos[elemento])
        listas[elemento].append(element.text)

# Fecha o navegador
navegador.quit()

# Cria o dataframe
df_resumo = pd.DataFrame(listas)
df_resumo['data'] = agora.date()
df_resumo['hora'] = agora.time()
df_resumo['periodo'] = ['Últimos 6 meses', 'Últimos 12 meses', 'Geral']

# Organiza colunas
df_resumo = df_resumo.iloc[:, [7, 8, 9, 0, 1, 2, 3, 4, 5, 6]]

# >>>> INSIRA AQUI O CAMINHO DO SEU ARQUIVO XLSX <<<<<
arquivo_registro = "D:/Faculdade/Challenge_Totvs_2025/Hermes.ai/registros.xlsx"

# Carrega a planilha
workbook = openpyxl.load_workbook(arquivo_registro)

# Seleciona a aba da planilha (corrigido para sintaxe atual)
sheet = workbook["registros"]

# Ajusta os tipos
df_resumo['data'] = pd.to_datetime(df_resumo['data']).dt.date

for i in range(3, 6):
    df_resumo.iloc[:, i] = df_resumo.iloc[:, i].astype(float)

for i in range(6, 9):
    df_resumo.iloc[:, i] = df_resumo.iloc[:, i].apply(
        lambda num: float(num.replace('%', '').replace(',', '.')) / 100
    )

df_resumo.iloc[:, 9] = df_resumo.iloc[:, 9].astype(float)

# Insere cada linha no arquivo Excel
for linha in df_resumo.values.tolist():
    sheet.append(linha)

# Salva as alterações
workbook.save(arquivo_registro)
