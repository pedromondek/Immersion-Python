# Aula 2: Importando biblioteca e Tabela Excel

from operator import le
from turtle import left
from pyparsing import col
import pandas as pd
import plotly.express as px

df_principal = pd.read_excel("tabela-acoes.xlsx", sheet_name="Principal")
df_principal.head(10)

df_total_acoes = pd.read_excel("tabela-acoes.xlsx", sheet_name="Total_de_acoes")
df_total_acoes

df_ticker = pd.read_excel("tabela-acoes.xlsx", sheet_name="Ticker")
df_ticker

df_chatgpt = pd.read_excel("tabela-acoes.xlsx", sheet_name="ChatGPT")
df_chatgpt

# Aula 3: Criando as colunas igual Excel & Analise

df_principal = df_principal[['Ativo', 'Data', 'Último (R$)', 'Var. Dia (%)']].copy()

df_principal = df_principal.rename(columns={'Último (R$)':'valor_final','Var. Dia (%)':'var_dia_pct'}).copy() 
df_principal['Var_pct'] = df_principal['var_dia_pct']/100

df_principal['valor_inicial'] = df_principal['valor_final']/(df_principal['Var_pct']+1)

df_principal = df_principal.merge(df_total_acoes, left_on='Ativo', right_on='Código', how='left')
df_principal = df_principal.drop(columns=['Código'])

df_principal['Variacao_rs']= df_principal['Var_pct'] = (df_principal['valor_final'] - df_principal['valor_inicial']) * df_principal['Qtde. Teórica']

pd.options.display.float_format = '{:.2f}'.format

df_principal['Qtde. Teórica'] = df_principal['Qtde. Teórica'].astype(int)

df_principal = df_principal.rename(columns={'Qtde. Teórica': 'qtd_teorica'}).copy()

df_principal['Resultado'] = df_principal['Variacao_rs'].apply(lambda x: 
                                                                'Subiu' if x > 0 
                                                                    else ('Desceu' if x < 0 
                                                                        else 'Estável'))

df_principal = df_principal.merge(df_ticker, left_on='Ativo', right_on='Ticker', how='left')
df_principal = df_principal.drop(columns=['Ticker'])

df_principal = df_principal.merge(df_chatgpt, left_on='Nome', right_on='Nome da Empresa', how='left')
df_principal = df_principal.drop(columns=['Nome da Empresa'])

df_principal = df_principal.rename(columns={'Idade (em anos)': 'idade'}).copy()

df_principal['Cat_Idade'] = df_principal['idade'].apply(lambda x: 
                                                            'Mais de 100' if x > 100 
                                                                else ('Menos de 50' if x < 50 
                                                                    else ('Indeterminado' if x == 'N/A' or x == 'Indeterminado' 
                                                                        else ('Entre 50 e 100'))))

df_principal

maior = df_principal['Variacao_rs'].max()
menor = df_principal['Variacao_rs'].min()
media = df_principal['Variacao_rs'].mean()

media_subiu = df_principal[df_principal['Resultado'] == 'Subiu']['Variacao_rs'].mean()
media_desceu = df_principal[df_principal['Resultado'] == 'Desceu']['Variacao_rs'].mean()

menor
maior
media
media_subiu
media_desceu

df_principal_subiu = df_principal[df_principal['Resultado'] == 'Subiu']
df_principal_subiu

df_analise_segmento = df_principal_subiu.groupby('Segmento')['Variacao_rs'].sum().reset_index()
df_analise_segmento

df_analise_saldo = df_principal.groupby('Resultado')['Variacao_rs'].sum().reset_index()
# df_analise_saldo['Variacao_rs'] = df_analise_saldo['Variacao_rs'].apply(lambda x: 'R${:,.2f}'.format(x))
df_analise_saldo

fig = px.bar(df_analise_saldo, x='Resultado', y='Variacao_rs', text='Variacao_rs', title='Variação Reais por Resultado')

# Desafio Aula 3
# 1 Pesquise com a documentação da biblioteca Plotly ou GPT como mudar a formatação dos números do gráfico de barras;

fig.update_yaxes(
    tickprefix="R$",
    tickformat=",.2f"
)

# 2 Fazer o gráfico de pizza no df_análise_segmentos com a mesma biblioteca Potly;

fig = px.pie(df_analise_segmento, values='Variacao_rs', names='Segmento', title='Variação Reais por Resultado')
fig.show()

# 3 Fazer o GroupBy da categoria de idades e gerar o gráfico de barras.

df_analise_idade = df_principal.groupby('Cat_Idade')['Variacao_rs'].sum().reset_index()
df_analise_idade


figIdade = px.bar(df_analise_idade, x='Cat_Idade', y='Variacao_rs', text='Variacao_rs', title='Variação Reais por Resultado')

figIdade.update_yaxes(
    tickprefix="R$",
    tickformat=",.2f"
)

figIdade.show()