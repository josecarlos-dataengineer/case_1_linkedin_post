
import pandas as pd
import numpy as np

pd.set_option('display.max_columns', 20)
pd.set_option('display.max_rows', 50)

# Qual faixa etária mais faz devoluções e trocas por estado e canal de compra?
df = pd.read_csv('example.csv',encoding='utf-8')

# Definindo a faixa_etaria
bins = [18, 30, 40, 50, 60, 70, 80, np.inf]
labels = ['18 +', '30 +', '40 +', '50 +', '60 +', '70 +', '80 +']
df['faixa_etaria'] = pd.cut(df['idade'], bins=bins, labels=labels, right=False)

# Calculate percentual_trocas_devolucoes
devolucoes_trocas_por_canal_estado = df.pivot_table(index=['estado', 'faixa_etaria', 'canal_venda'],
                                                    columns='operacao',
                                                    values='quantidade',
                                                    aggfunc='sum').reset_index()
devolucoes_trocas_por_canal_estado['percentual_trocas_devolucoes'] = \
    (devolucoes_trocas_por_canal_estado['devolução'] + devolucoes_trocas_por_canal_estado['troca']) \
    / devolucoes_trocas_por_canal_estado['compra'] * 100

devolucoes_trocas_por_canal_estado.dropna(inplace=True)
# Top 10 results
resposta = devolucoes_trocas_por_canal_estado.sort_values(by='percentual_trocas_devolucoes', ascending=False)

resposta[['estado','faixa_etaria','canal_venda','percentual_trocas_devolucoes']].reset_index()
