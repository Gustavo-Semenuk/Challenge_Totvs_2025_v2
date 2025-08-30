import pandas as pd
import numpy as np

df = pd.read_excel(
    r'C:\Users\Gustavo\Downloads\Dados Abertos\PAC - Pesquisa Anual de Comércio\tabelas_2021_xlsx\XLS\Tabela 1.xlsx', sheet_name='TAB01A', skiprows=8)

print(df.head())